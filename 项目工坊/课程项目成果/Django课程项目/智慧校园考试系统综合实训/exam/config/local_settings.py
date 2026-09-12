DEBUG = True
DOMAIN = 'http://127.0.0.1:8000'
ALLOWED_HOSTS = ['*']
BANK_REPO = r'backup'  # 设置题库上传路径
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}
# send e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465   # 465 SSL端口   587  # TLS端口

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

EMAIL_USE_SSL = True  # 必须为True
EMAIL_USE_TLS = False  # 必须为False（与SSL互斥）
# Email address that error messages come from.
# Default email address to use for various automated correspondence from
# the site managers.
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# People who get code error notifications.
# In the format [('Full Name', 'email@example.com'), ('Full Name', 'anotheremail@example.com')]
# ADMINS = [('zhang8680@outlook.com'),]
# Not-necessarily-technical managers of the site. They get broken link
# notifications and other various emails.
# MANAGERS = ADMINS

# 管理员设置（需要是元组列表）
ADMINS = [('管理员', 'zhang8680@outlook.com'),]
MANAGERS = ADMINS

