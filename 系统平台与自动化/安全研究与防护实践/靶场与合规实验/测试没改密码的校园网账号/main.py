import re

import requests

# 1. 提交的目标 URL（根据 ee 函数和系统特征推测）
# 推荐使用这个地址，它是认证系统API的典型地址
FINAL_LOGIN_URL = "http://10.20.3.1:801/eportal/?c=ACSetting&a=Login"


# 2. 构造 POST 请求的数据负载
# 这些参数会被 login.init(form) 收集并发送
data = {
    'DDDDD': '',  # 账号
    'upass': '',  # 密码（注意：如果密码长度大于16位，客户端会进行截断，您需要自行处理）
    '0MKKey': '登录',  # 登录按钮的值（虽然是按钮，但有些系统也会把按钮值作为参数）
}

# 3. 设置请求头（模拟浏览器）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',  # 推荐使用完整的浏览器UA
    'Content-Type': 'application/x-www-form-urlencoded',
    "Origin": "http://10.20.3.1",
    # 关键：设置 Referer 头，告诉服务器请求来自哪个页面
    'Referer': 'http://10.20.3.1/a79.htm?wlanacip=10.20.3.254'
}
# 登陆失败字典
error_messages = {
    "01": "认证失败 - 账号或密码错误",
    "02": "账号已在线",
    "03": "账号被禁用",
    "04": "账号余额不足",
    "05": "账号过期",
    "06": "MAC地址绑定错误",
    "07": "IP地址绑定错误",
    "08": "在线用户数超限"
}


# 4. 发送 POST 请求
try:
    response = requests.post(FINAL_LOGIN_URL, data=data, headers=headers, timeout=10)

    # 检查登录结果
    if response.status_code == 200:
        # 认证成功可能返回成功提示(JSON数据)
        print(response.text)
        if re.search("<!--Dr.COMWebLoginID_2.htm-->", response.text):
            # 匹配是否成功
            match = re.search(r"Msg=(\d{2});", response.text).group(1)
            print(error_messages[match])



    else:
        print(f"请求失败，状态码：{response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"发生网络错误: {e}")