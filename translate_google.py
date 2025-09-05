from googletrans import Translator

def trans_to_chinese_by_google(txt):
    
    translator = Translator()
    result = translator.translate(txt, dest='zh-tw')
    return result.text