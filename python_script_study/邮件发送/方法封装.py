# 获取系统变量
import os
# smtplib 是 Python 内置的 SMTP 协议客户端库，用于连接邮件服务器并发送邮件
import smtplib
from datetime import time
# MIMEText 用于构造纯文本或 HTML 格式的邮件正文内容（MIME 是邮件扩展标准，定义邮件格式）
from email.mime.text import MIMEText
# MIMEImage 用于构造图片附件
from email.mime.image import MIMEImage
# MIMEMultipart 用于构造包含多个部分（如正文、附件等）的复合邮件对象
from email.mime.multipart import MIMEMultipart
# 随机数生成
import random
# 时间获取
from datetime import datetime


def send_verification_email(email: str, verification_num: str):
    # 创建一个 MIMEMultipart 多部分邮件容器对象，可以容纳正文、附件等多种内容块
    msg = MIMEMultipart('related')  # 必须有参数'related' 多部分邮件容器对象
    # 设置邮件头部的「发件人」、「收件人」、「主题」
    msg["From"] = os.getenv("SENDER_EMAIL", "")
    msg["To"] = email
    msg["Subject"] = "验证码"

    # 验证码模板
    with open("email_template.html", "r", encoding="utf-8") as f:
        html_template = f.read()
        # 替换验证码内容
    html_template = html_template.replace("{verification_code}", verification_num)
    # 替换时间内容
    html_template = html_template.replace("{time}", f"{datetime.now().year}")
    # 替换发送方名称(app名称)
    html = html_template.replace("{app_name}", "ACG鉴赏图廊")
    msg.attach(MIMEText(html, "html"))
    # 附加图片
    with open("logo.png", "rb") as f:
        img = MIMEImage(f.read())
    img.add_header("Content-ID", "<logo>")
    msg.attach(img)

    try:
        # 使用 SMTP_SSL 通过 SSL 加密方式连接到 QQ 邮箱的 SMTP 服务器（使用 with 语句确保连接用完后自动关闭）
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            # 使用发件人邮箱地址和授权码登录 SMTP 服务器，完成身份认证（未认证则无法发送邮件）
            server.login(os.getenv("SENDER_EMAIL", ""), os.getenv("SMTP", ""))
            # 调用 sendmail 方法发送邮件：参数依次为 发件人地址、收件人地址、邮件完整内容（as_string() 将 MIMEMultipart 对象序列化为符合 SMTP 协议的字符串）
            server.sendmail(os.getenv("SENDER_EMAIL", ""), email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print({"message": "授权码错误或未开启 SMTP 服务"})
    except ConnectionRefusedError:
        print({"message": "网络不通或端口被防火墙拦截"})
    except Exception as e:
        print({"message": e})
    else:
        # 邮件发送成功后，在控制台打印一个字典格式的成功提示信息
        print({"message": "邮件发送成功"})

if __name__ == '__main__':
    # 添加邮箱的环境变量
    os.environ['SENDER_EMAIL'] = "自己的QQ邮箱"
    # 添加授权码的环境变量
    os.environ['SMTP'] = "自己去QQ邮箱里找"
    # 发送邮件
    send_verification_email("接收者的邮箱(对面)", ''.join(random.choices('0123456789', k=6)))