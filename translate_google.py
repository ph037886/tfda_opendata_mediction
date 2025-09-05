from googletrans import Translator

def translate_text(txt):
    translator = Translator()
    result = translator.translate(str(txt), dest='zh-TW')  # zh-TW = 繁體中文
    return result.text