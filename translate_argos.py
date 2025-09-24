import argostranslate
import pathlib

def update_argos():
    
    # Download and install Argos Translate package
    from_code = "en"
    to_code = "zh"
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

def trans_to_chinese_by_argos(txt):
    #語言轉換代碼 https://www.argosopentech.com/argospm/index/
    from_code = "en"
    to_code = "zt" #繁體中文
    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    # Translate
    translatedText = argostranslate.translate.translate(txt, from_code, to_code)
    #print(translatedText)
    #print(type(translatedText))
    return translatedText

def dict_argosmodel_path(lang):
    from_to_argosmodel={'en_ja':'translate-en_ja-1_1.argosmodel',
                        'en_ko':'translate-en_ko-1_1.argosmodel',
                        'en_th':'translate-en_th-1_9.argosmodel',
                        'en_zt':'translate-en_zt-1_9.argosmodel',
                        'ja_en':'translate-ja_en-1_1.argosmodel',
                        'ko_en':'translate-ko_en-1_1.argosmodel',
                        'th_en':'translate-th_en-1_9.argosmodel',
                        'zt_en':'translate-zt_en-1_9.argosmodel',
                        'zh_en':'translate-zh_en-1_9.argosmodel'}
    return from_to_argosmodel[lang]

def trans_with_argos_offline(from_lang, to_lang, text):
    lang_name_to_code={'正體中文':'zt',
                       '英文':'en',
                       '日文':'ja',
                       '韓文':'ko',
                       '泰文':'th',
                       '簡體中文':'zh'}
    
    from_code = lang_name_to_code[from_lang]
    to_code = lang_name_to_code[to_lang]
    argosmodel_path='files/argosmodel/'
    argosmodel_path=argosmodel_path + dict_argosmodel_path(from_code+'_'+to_code)
    package_path = pathlib.Path(argosmodel_path)
    argostranslate.package.install_from_path(package_path)
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    return translatedText
