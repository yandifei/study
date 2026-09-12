# constants.py 或直接在views.py中定义
VeriCodeTimeOut = {
    'error_code': 4001,
    'error_msg': '验证码已过期，请重新获取',
    'redirect_url': '/auth/resend-activation/',
    'redirect_time': 5,
}

VeriCodeError = {
    'error_code': 4002,
    'error_msg': '验证码错误',
    'redirect_url': '/',
    'redirect_time': 3,
}

VerifyFailed = {
    'error_code': 4003,
    'error_msg': '用户验证失败',
    'redirect_url': '/register/',
    'redirect_time': 5,
}

ActivationSuccess = {
    'success_code': 2001,
    'success_msg': '账户激活成功',
    'redirect_url': '/',
    'redirect_time': 3,
}