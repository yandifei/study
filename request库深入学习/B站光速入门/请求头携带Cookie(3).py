import requests

# SSL证书验证失败：
# 错误信息 ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] 表明Python无法验证GitHub的SSL证书
# 核心原因是 unable to get local issuer certificate - 系统缺少验证证书链所需的根证书
# 常见触发场景：
# Windows系统未更新根证书
# Python环境（尤其是Anaconda）未正确配置SSL证书路径
# 企业防火墙/代理拦截了SSL连接

# 1.使用certifi的CA证书包(我电脑显示找不到证书)
# import certifi
# response = requests.get(url, headers=headers, verify=certifi.where())
# 2.
# 下载最新根证书包：
# https://curl.se/ca/cacert.pem
# response = requests.get(url, headers=headers, verify=证书路径)
# response = requests.get(url, headers=headers, verify="./cacert.pem")
# 3.这个能用
# 临时禁用证书验证（测试环境用）
# response = requests.get(url, headers=headers, verify=False)
# 问题解析
# proxies = {"https": "http://user:pass@corp-proxy:port"} # 配置代理证书(如果使用公司/学校网络，可能需要配置代理证书)

# 我的Github地址
url = "https://github.com/yandifei"

# 构建请求头
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Cookie": "_octo=GH1.1.7383981.1744609068; _device_id=e8995a13927ac6ff03d41002c1825ac0; saved_user_sessions="
              "178072152%3AvSxlmMLzOyRm7HDmPQ1XpJgtbcslmKZGoZzVQmwwV1x1McBt; user_session=vSxlmMLzOyRm7HDmPQ1XpJg"
              "tbcslmKZGoZzVQmwwV1x1McBt; __Host-user_session_same_site=vSxlmMLzOyRm7HDmPQ1XpJgtbcslmKZGoZzVQmwwV"
              "1x1McBt; logged_in=yes; dotcom_user=yandifei; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22lig"
              "ht_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%"
              "3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_colo"
              "r_mode=light; tz=Asia%2FShanghai; _gh_sess=Xdq68Zxd5R4KtOwjYQRvfAWBD3eq6eeETnVnhbF8lIEAoAOnBYRSljP"
              "gkeo%2FXoZju7dJqLTn2n1dPHiVju%2BavTDgud2SfMVB%2FF6IfZUBt1Nx4FiJ7%2BdLSwSeySPOnSsgg0qPWNCtCnFiK6B4L"
              "ZsOuo99F1mM%2BwgBVnhCtBA26MMUV7w8%2FNQWd7TvT%2Bu66lg9TYStZ43UBVatbAWYaJucjGcOLIhWIEJ62Qj7PehvzGmD4"
              "NGwKzj2X0v5EBGmAMH%2BXoZicA0NB78jxlJooXmNnex33jWvsY0vYYDIUy3aeHlGNd57RZpFCPcXUZZW5%2BCvGoPXVmGz7ZD"
              "8aJfzpMrbXEWYFtbSBXvRkCkDSOWb2z1s0EA3zsOdIe3MAreWgFRD--x7IgitQtXE6NbEG%2F--0W%2BYFB5HHE14uYYj%2B7T"
              "yIA%3D%3D"
}

# 构建请求（verify直接禁用）
response = requests.get(url, headers=headers,verify=False)

# 以二进制的形式写入html文件
with open("github_cookies.html", "wb") as f:
    f.write(response.content)   # 把内容写入进去

