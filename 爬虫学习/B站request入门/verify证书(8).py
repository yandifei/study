"""
使用verify参数忽略CA证书
使用这种非官方证书的网站后的提示(以下是浏览器，如果是requests的话会报错)：
    您的连接不是私密连接
    攻击者可能会试图从wWw.12306.cn窃取您的信息（例如：密码、通讯内容或信用卡信
    息）。了解详情
    NET:ERR_CERT_COMMON_NAME_INVALID
    白动向Google发送一些系统信息和网页内容，以帮助检测危险应用和网站。隐私权政策
    隐藏详情
    返回安全连接
    此服务器无法证明它是www.12306.cn;其安全证书来自webssl.chinanetcenter.com。
    出现此问题的原因可能是配置有误或您的连接被拦截了。
如：
https://sam.huat.edu.cn:8443/selfservice/
通常禁止使用CA证书就行，最多报个警告
"""

import requests
url = "https://sam.huat.edu.cn:8443/selfservice/"

response = requests.get(url, verify=False)

print(response.content)
