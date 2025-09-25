import argostranslate.package
import argostranslate.translate
import pathlib
from opencc import OpenCC

def update_argos(from_code, to_code):
    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

def ensure_package_installed(package_path: str):
    package_path = pathlib.Path(package_path)
    installed = argostranslate.package.get_installed_packages()
    # 依需要檢查是否已安裝對應語對；簡化處理：直接安裝一次即可（已裝會跳過）
    argostranslate.package.install_from_path(package_path)

def offline_argosmodel_install(lang_code):
    #argosmodel網址：https://www.argosopentech.com/argospm/index/
    from_to_argosmodel={'en_ja':'translate-en_ja-1_1.argosmodel',
                        'en_ko':'translate-en_ko-1_1.argosmodel',
                        'en_th':'translate-en_th-1_9.argosmodel',
                        'en_zt':'translate-en_zt-1_9.argosmodel',
                        'ja_en':'translate-ja_en-1_1.argosmodel',
                        'ko_en':'translate-ko_en-1_1.argosmodel',
                        'th_en':'translate-th_en-1_9.argosmodel',
                        'zt_en':'translate-zt_en-1_9.argosmodel',
                        'zh_en':'translate-zh_en-1_9.argosmodel'}
    argosmodel_path='files/argosmodel/'     
    argosmodel_path=argosmodel_path + from_to_argosmodel[lang_code]
    package_path = pathlib.Path(argosmodel_path)
    argostranslate.package.install_from_path(package_path)
        
def check_install_choose(from_code, to_code):
    if (from_code!='en') and (to_code!='en'):
        print('非直接翻譯語言，為原始語言翻譯為英文，再由英文翻譯為目標語言。\n')
        offline_argosmodel_install(from_code+'_en')
        offline_argosmodel_install('en_'+to_code)
    else:
        offline_argosmodel_install(from_code+'_'+to_code)

def lang_code_map():
    lang_name_to_code={'正體中文':'zt',
                       '英文':'en',
                       '日文':'ja',
                       '韓文':'ko',
                       '泰文':'th',
                       '簡體中文':'zh'}
    return lang_name_to_code

def post_process(text):
    term_map = {'抑制剂': '抑制劑', '炎症': '發炎'}  # 只是示意
    for k, v in term_map.items():
        text = text.replace(k, v)
    return text

def trans_with_argos_offline(from_lang, to_lang, text):
    lang_name_to_code=lang_code_map()
    from_code = lang_name_to_code[from_lang]
    to_code = lang_name_to_code[to_lang]
    #offline_argosmodel_install(from_code, to_code)
    check_install_choose(from_code, to_code)
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    if to_code=='zt':
        cc=OpenCC('s2twp') #argos轉換出來會簡繁夾雜，使用opencc做簡繁體轉換
        translatedText=cc.convert(translatedText)
        #post_process(translatedText) #後處理器，可以用於一些特殊字詞修改，未實裝
    return translatedText

if __name__=='__main__':
    lang_name_to_code=lang_code_map()
    lang_name_list=list(lang_name_to_code.keys())
    i=1
    for in_lang in lang_name_list:
        print(f'{i}. {in_lang}')
        i+=1
    in_lang=int(input('選擇輸入語言：'))
    in_lang=lang_name_list[in_lang-1]
    print('\n')
    i=1
    for out_lang in lang_name_list:
        print(f'{i}. {out_lang}')
        i+=1
    out_lang=int(input('選擇輸入語言：'))
    out_lang=lang_name_list[out_lang-1]
    print('\n')
    txt=input('請輸入文字：')
    print('\n翻譯中，請稍後~\n')
    print(trans_with_argos_offline(in_lang, out_lang, txt))