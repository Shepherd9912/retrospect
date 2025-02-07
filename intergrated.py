import cv2
from openai import OpenAI
import os
from PIL import ImageGrab
import pytesseract
import requests
import tkinter as tk

# my deepseek api id: ds_translator_proposedby_shepherd9912_7_2_25
DEEPSEEK_API_KEY = "" # 替换成自己的

# 截屏，再截图
def screen_shot():
    screenshot = ImageGrab.grab()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    print(f"截图已保存到：{screenshot_path}\n")

bbox = [] # 点坐标的列表

def mouse_callback(event, x, y, flags, userdata):
    # 如果鼠标左键点击，则输出横坐标和纵坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox.append(x)
        bbox.append(y)
        print('截图区域：', f'({x}, {y})\n')

def picture_shot():
    screen_shot()
    global bbox
    img = cv2.imread("screenshot.png")
    # 创建窗口
    cv2.namedWindow('Point Coordinates', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Point Coordinates', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # 将回调函数绑定到窗口
    cv2.setMouseCallback('Point Coordinates', mouse_callback)
    # 显示图像
    while True:
        cv2.imshow('Point Coordinates', img)
        k = cv2.waitKey(1) & 0xFF
        # 按esc键退出
        # if (len(bbox) == 4) | (k == 27):
        if (len(bbox) >= 4) | (k == 27):
            # start_x, start_y, end_x, end_y = bbox            
            break
    cv2.destroyAllWindows()
    try:
        start_x, start_y, end_x, end_y = bbox
        screenshot = ImageGrab.grab(bbox = (start_x, start_y, end_x, end_y))
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)           
        bbox = []
        return screenshot_path
    except Exception as e:
        print(f"截图失败: {str(e)}\n")
        return ""

def pre_process(filename):
    image = cv2.imread(filename)
    # cv2.imshow('my_window', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # 自适应阈值
    #binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 反色
    inverted = cv2.bitwise_not(binary)
    processed_img = cv2.bitwise_not(inverted)
    denoised = cv2.medianBlur(binary, 3)
    # 定义结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # 膨胀操作
    dilated = cv2.dilate(denoised, kernel, iterations=1)
    # 腐蚀操作
    eroded = cv2.erode(dilated, kernel, iterations=1)
    # 调整对比度和亮度
    alpha = 1.5  # 对比度
    beta = 0     # 亮度
    adjusted = cv2.convertScaleAbs(eroded, alpha=alpha, beta=beta)
    # 保存预处理后的图像
    preprocessed_path = "preprocessed.png"
    cv2.imwrite(preprocessed_path, processed_img)
    return preprocessed_path
    
    # 显示预处理后的图像
    # cv2.imshow("Preprocessed Image", processed_img)

def recognize_words(filename):
    pytesseract.pytesseract.tesseract_cmd = r"D:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Tesseract路径
    text = pytesseract.image_to_string(filename, lang='jpn+jpn_vert')  # 支持中英文
    print("识别到的文字：", text, "\n")
    return text

def translate_with_ds_sort1(text): # deepseek官方档案给的格式
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
      
    # my deepseek api id: ds_translator_proposedby_shepherd9912_7_2_25

    if not text:
        return ""

    client = OpenAI(api_key = DEEPSEEK_API_KEY, base_url = DEEPSEEK_API_URL)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text into simplified chinese. The text is from a galgame, お兄ちゃん頑張って!"},
            {"role": "user", "content": f"Translate the following text: {text}"},
        ],
        stream=False
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content

def translate_with_ds_sort2(text): # 问deepseek生成的格式
    """调用DeepSeek进行翻译"""
    if not text:
        return ""
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that translates text into simplified chinese. The text is from a galgame, お兄ちゃん頑張って!"},
            {"role": "user", "content": f"将以下内容精确翻译为中文，只需返回译文：{text}"}
        ],
        "model": "deepseek-chat",
        "temperature": 0.1  # 降低随机性
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"翻译失败: {str(e)}\n")
        return ""

def delete_temp(screenshot_path, processed_image_path):
    # 删除截图文件
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
        print(f"已删除截图文件：{screenshot_path}\n")
    
    # 删除处理后的图像文件
    if os.path.exists(processed_image_path):
        os.remove(processed_image_path)
        print(f"已删除处理后的图像文件：{processed_image_path}\n")

def refresh_gui(translation):
    # 更新 GUI 显示
    translation_label.config(text=translation)

def translate_execute():
    try:
        if hasattr(translate_execute, "processing") and translate_execute.processing:
            return  # 防止重复触发
        translate_execute.processing = True

        screenshot_path = picture_shot()
        preprocessed_path = pre_process(screenshot_path)
        text = recognize_words(preprocessed_path)
        consequence = translate_with_ds_sort1(text)
        print(consequence)
        refresh_gui(consequence)
        delete_temp(screenshot_path, preprocessed_path)

        translate_execute.processing = False  # 允许再次触发
    except Exception as e:
        print(f"运行时发生错误: {str(e)}\n")
        translate_execute.processing = False  # 确保即使发生错误也能继续触发

if __name__ == '__main__':

    # GUI 界面
    root = tk.Tk()
    root.title("实时屏幕截图翻译器")

    # 显示翻译结果的标签
    translation_label = tk.Label(root, text = "翻译结果将显示在这里", wraplength = 400)
    translation_label.pack()

    # 开始翻译按钮
    translate_button = tk.Button(root, text = "开始翻译", command = translate_execute)
    translate_button.pack()

    root.mainloop()

