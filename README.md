# ds_translator_V_1

ds_translator是截屏、识文、翻译的三合一的翻译器


技术路线：


（1）截图：和qq一样，先截图桌面，在大图的基础上截取小图。截图方法为点一下截取范围的左上角和右下角。

（2）识文：使用OpenCV对截取的文字进行预处理，使用OCR库识别文字，目前准确率较低

（3）翻译：调用deepseek api接口，使用前需在代码里补全个人的deepseek api key，具体调用函数有两种，一种是源于deepseek官方文档，另一种由deepseek生成，后者可以修改temperature


后期工作：


（1）优化ui

（2）进行更为有效的CV预处理

# 使用方法

```python
def recognize_words(filename):
    pytesseract.pytesseract.tesseract_cmd = r"D:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Tesseract路径
    text = pytesseract.image_to_string(filename, lang='jpn+jpn_vert')  # 支持中英文
    print("识别到的文字：", text, "\n")
    return text
```
上述代码中tesseract_cmd改为自己电脑tsseract所在位置，另外可以通过lang设置识别语言，支持的语言如下，多种语言以+号连接
```bash
langs: ['afr', 'amh', 'ara', 'asm', 'aze', 'aze_cyrl', 'bel', 'ben', 'bod', 'bos', 'bre', 'bul', 'cat', 'ceb', 'ces', 'chi_sim', 'chi_sim_vert', 'chi_tra', 'chi_tra_vert', 'chr', 'cos', 'cym', 'dan', 'deu', 'deu_latf', 'div', 'dzo', 'ell', 'eng', 'enm', 'epo', 'equ', 'est', 'eus', 'fao', 'fas', 'fil', 'fin', 'fra', 'frm', 'fry', 'gla', 'gle', 'glg', 'grc', 'guj', 'hat', 'heb', 'hin', 'hrv', 'hun', 'hye', 'iku', 'ind', 'isl', 'ita', 'ita_old', 'jav', 'jpn', 'jpn_vert', 'kan', 'kat', 'kat_old', 'kaz', 'khm', 'kir', 'kmr', 'kor', 'lao', 'lat', 'lav', 'lit', 'ltz', 'mal', 'mar', 'mkd', 'mlt', 'mon', 'mri', 'msa', 'mya', 'nep', 'nld', 'nor', 'oci', 'ori', 'osd', 'pan', 'pol', 'por', 'pus', 'que', 'ron', 'rus', 'san', 'sin', 'slk', 'slv', 'snd', 'spa', 'spa_old', 'sqi', 'srp', 'srp_latn', 'sun', 'swa', 'swe', 'syr', 'tam', 'tat', 'tel', 'tgk', 'tha', 'tir', 'ton', 'tur', 'uig', 'ukr', 'urd', 'uzb', 'uzb_cyrl', 'vie', 'yid', 'yor']
```
