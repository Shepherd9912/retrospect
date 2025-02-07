# ds_translator_V_1

ds_translator是截屏、识文、翻译的三合一的翻译器
技术路线：
（1）截图：和qq一样，先截图桌面，在大图的基础上截取小图。截图方法为点一下截取范围的左上角和右下角。
（2）识文：使用OpenCV对截取的文字进行预处理，使用OCR库识别文字，目前准确率较低
（3）翻译：调用deepseek api接口，使用前需在代码里补全个人的deepseek api key，具体调用函数有两种，一种是源于deepseek官方文档，另一种由deepseek生成，后者可以修改temperature
后期工作：
（1）优化ui
（2）进行更为有效的CV预处理
