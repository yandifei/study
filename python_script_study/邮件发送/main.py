# smtplib 是 Python 内置的 SMTP 协议客户端库，用于连接邮件服务器并发送邮件
import os
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

# 【使用前必须修改的配置】
#   → SENDER_EMAIL：替换为你的真实 QQ 邮箱
#   → AUTHORIZATION_CODE：替换为你在 QQ 邮箱生成的授权码
#   → email：替换为收件人的真实邮箱地址
#   → code：替换为随机生成的验证码（建议使用 random 模块）

# ==================== 邮件服务器配置 ====================
# QQ 邮箱的 SMTP 服务器地址，所有通过 QQ 邮箱发送的邮件都需要经过此服务器中转
SMTP_SERVER = "smtp.qq.com"
# SMTP_SSL 加密连接所使用的端口号（465 端口使用 SSL/TLS 加密传输，保证通信安全）
SMTP_PORT = 465
# 发件人的 QQ 邮箱地址，需要替换为真实的 QQ 邮箱（格式：QQ号@qq.com）
SENDER_EMAIL = "3646917783@qq.com"
# QQ 邮箱的 SMTP 授权码（非 QQ 密码），需要在 QQ 邮箱网页端 → 设置 → 账户 → POP3/SMTP 服务中开启并生成
AUTHORIZATION_CODE: str =  os.getenv("SMTP", "")

# ==================== 收件人与验证码配置 ====================
# 收件人邮箱地址（注意：当前值为整数 1，实际使用时需替换为有效的邮箱字符串，如 "example@163.com"）
email: str = "2171872836@qq.com"

# ==================== 构造邮件内容 ====================
# 创建一个 MIMEMultipart 多部分邮件容器对象，可以容纳正文、附件等多种内容块
msg = MIMEMultipart()
# 设置邮件头部的「发件人」字段，显示在收件人邮箱中的发送者地址
msg["From"] = SENDER_EMAIL
# 设置邮件头部的「收件人」字段，指定这封邮件要发送给哪个邮箱地址
msg["To"] = email
# 设置邮件的「主题」，即收件人在收件箱列表中看到的邮件标题
msg["Subject"] = "验证码"

# # 使用 f-string 格式化邮件正文内容，将验证码变量 code 动态插入到文本模板中
# body = f"您的验证码是：{code}，有效期5分钟。"
# # 将正文内容包装为 MIMEText 对象（"plain" 表示纯文本格式，若需要富文本可改为 "html"），并附加到邮件容器中
# msg.attach(MIMEText(body, "html"))

# 验证码模板
with open("email_template.html", "r", encoding="utf-8") as f:
    html_template = f.read()
    # 替换验证码内容
html_template = html_template.replace("{verification_code}", ''.join(random.choices('0123456789', k=6)))
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

# ==================== 进行发送操作 ====================
try:
    # 使用 SMTP_SSL 通过 SSL 加密方式连接到 QQ 邮箱的 SMTP 服务器（使用 with 语句确保连接用完后自动关闭）
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        # 使用发件人邮箱地址和授权码登录 SMTP 服务器，完成身份认证（未认证则无法发送邮件）
        server.login(SENDER_EMAIL, AUTHORIZATION_CODE)
        # 调用 sendmail 方法发送邮件：参数依次为 发件人地址、收件人地址、邮件完整内容（as_string() 将 MIMEMultipart 对象序列化为符合 SMTP 协议的字符串）
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
except smtplib.SMTPAuthenticationError:
    print({"message": "授权码错误或未开启 SMTP 服务"})
except ConnectionRefusedError:
    print({"message": "网络不通或端口被防火墙拦截"})
except Exception as e:
    print({"message": e})
else:
    # 邮件发送成功后，在控制台打印一个字典格式的成功提示信息
    print({"message": "邮件发送成功"})
