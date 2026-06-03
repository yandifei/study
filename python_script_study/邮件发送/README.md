# 邮箱验证码发送
## 配置
这里是写必要的配置:
1. SMTP码，放到环境变量`SMTP`
2. 环境变量`SENDER_EMAIL`设置你的QQ邮箱
3. 确保`email_template.html`、`logo.png`、`方法封装.py`这三个文件存在

### QQ邮箱拿到SMTP码
SMTP码可以简单理解为邮箱密码，所以绝对不能泄露。
别人拿到SMTP码就可以登录你的邮箱并发送删除邮件了

QQ获取SMTP码：
https://wx.mail.qq.com/
登录后右上角点击设置
点击账号与安全后会跳转界面
在跳转界面中点击安全设置 在这个界面中你就能看到"POP3/IMAP/SMTP/Exchange/CardDAV 服务"这个内容了
点击生成授权码，之后会要你发送短信验证或者接收短信验证
验证后就会给你授权码，记住你得马上复制并放到安全的地方(我临时创了一个1.txt文件放了进去，后面放到了系统用户变量里)，他后面不给你复制和查看这个授权码的机会了，所以要立刻包存
最后就是给这个授权码取个名字方便我们知道他用来干啥的，我这里取名是"邮件发送"

### SMTP码泄露处理
访问：https://wx.mail.qq.com/
登录后右上角点击设置
点击账号与安全后会跳转界面
在跳转界面中点击设备管理，
点击授权码管理就会看到所有的SMTP了
点击需要停用的那个，只有1个就代表就是这个了

### 代码的配置
添加邮箱的环境变量
os.environ['SENDER_EMAIL'] = "发送者的邮箱"
添加授权码的环境变量
os.environ['SMTP'] = "SMTP"
调用方法
send_verification_email("接收者的邮箱", ''.join(random.choices('0123456789', k=6)))


## 模板修改
`ACG鉴赏图廊`改成你自己写的服务、软件名、app名就行
```python
html = html_template.replace("{app_name}", "ACG鉴赏图廊")
```
然后可以替换图标`logo.png`，名字不要改变就行

## 必要的文件
`email_template.html`
`logo.png`
`方法封装.py`