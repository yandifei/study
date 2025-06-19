"""实战演练
视频学习：
【Python3的requests库使用教程】https://www.bilibili.com/video/BV1UR4y1p7s6?p=15&vd_source=298465310cd98e6ceddf1afe7d72e7ec
个人总结：
今天是2025-6-19，这个视频里的部分内容的网址已经失效，例如金山翻译上了加密，然后就是GitHub也升级了。
这加大了我的难度，中途遇到了挺多问题的，像是无法访问GitHub的问题(我开了Stream++还是显示我证书问题，后面也尝试解决)
GitHub的请求参数变多了，这也是遇到的困难
"""
import datetime

import requests
import re   # 导入正则

def login(account, password):
    """GitHub登录
    account ： 账号
    password ： 密码
    """
    # session对象保持对话
    session = requests.session()
    session.verify = False  # 全程禁用证书

    # headers(这里直接用session的headers设置)
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }

    # url1-获取token
    url1 = "https://github.com/login"
    # 发送请求获取响应
    res1 = session.get(url1).content.decode()   # 获得二进制内容并进行解码
    # print(res1)
    # 正则提取所需要的数据(authenticity_token、 timestamp、timestamp_secret 、 required_field_xxxx)
    authenticity_token = re.findall('name="authenticity_token" value="(.*?)" />',res1)[0]   # 正则，res1是html数据
    timestamp = re.findall('<input class="form-control" type="hidden" name="timestamp" value="(.*?)" />', res1)[0]  # 正则，res1是html数据
    timestamp_secret = re.findall('<input class="form-control" type="hidden" name="timestamp_secret" value="(.*?)" />', res1)[0]  # 正则，res1是html数据
    required_field_num = re.findall('<input class="form-control" type="text" name="(.*?)" hidden="hidden" />', res1)[0]  # 正则，res1是html数据
    # print(f"动态获取的信息：{authenticity_token = }, {timestamp = },{timestamp_secret = },{required_field_num = }")

    # url2-登录
    url2 = "https://github.com/session"
    # 构建表单数据
    data = {
        "commit": "Sign in",
        "authenticity_token": authenticity_token,
        "add_account": "",
        "login": account,
        "password": password,
        "webauthn-conditional": "undefined",
        "javascript-support": "true",
        "webauthn-support": "supported",
        "webauthn-iuvpaa-support": "supported",
        "return_to": "https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home",
        "allow_signup": "",
        "client_id": "",
        "integration": "",
        required_field_num: "",
        "timestamp": timestamp,
        "timestamp_secret": timestamp_secret
    }
    # 发送请求登录
    session.post(url2, data=data)
    url2_html = session.get("https://github.com/").content.decode()     # 获得登录后html的源码
    # print(url2_html)
    # 构建url3的仓库地址(拼接链接)
    GitHub_name = re.findall('<meta name="octolytics-actor-login" content="(.*?)" />', url2_html)[0]
    # print(GitHub_name)

    # url3-验证
    url3 = f"https://github.com/{GitHub_name}"    # 我仓库的地址
    response = session.get(url3)
    with open("github.html", "wb") as f:
        f.write(response.content)
    print("github.html写入完成")

    # 判断登录是否成功（查看html的标记）
    title = re.findall("<title>(.*?)</title>", response.content.decode())[0]
    # 登录未成功就会有这个
    if " · GitHub" in title:
        print(f"用户：{GitHub_name} 登录失败")
    else:
        print(f"用户：{GitHub_name} 登录成功")

    # 判断你今天有没有写代码
    # 拿到今天的时间
    time = datetime.datetime.now().strftime("%Y-%m-%d")
    jude_flag = re.findall(f'data-date="{time}" id="contribution-day-component[^"]*" data-level="(.*?)" role="gridcell"',response.content.decode())[0]
    # print(jude_flag)
    if jude_flag == "0":
        print("你今天没有提交代码")
    else:
        print("你今天提交代码了")

if __name__ == '__main__':
    # 这里有可能触发你的GitHub双重认证以及验证码
    login()
