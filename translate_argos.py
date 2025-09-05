import argostranslate.package
import argostranslate.translate

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