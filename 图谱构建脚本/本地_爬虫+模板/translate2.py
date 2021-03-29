# encoding: utf-8

from translate import Translator
translator= Translator(from_lang="chinese",to_lang="english")
translation = translator.translate("在anconda3下找到Anaconda Prompt终端平台，输入pip install translate，这里的translate包是微软的，翻译良好。等待安装完成即可")
print(translation)