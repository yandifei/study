# 使用 cookies 参数保持会话
# 注意：cookies一般是有过期时间的，一旦过期需要重新获取
# 之前是在 headers 里带上 Cookie 这个字段，现在是使用它
import requests

# 我的Github地址
url = "https://github.com/yandifei"

# 构建请求头
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}

# 将 Cookie 字符串转为字典（cookies参数需要）
Cookie = ("_octo=GH1.1.7383981.1744609068; "
          "_device_id=e8995a13927ac6ff03d41002c1825ac0; "
          "saved_user_sessions=178072152%3AvSxlmMLzOyRm7HDmPQ1XpJgtbcslmKZGoZzVQmwwV1x1McBt; "
          "user_session=vSxlmMLzOyRm7HDmPQ1XpJgtbcslmKZGoZzVQmwwV1x1McBt; __Host-user_session"
          "_same_site=vSxlmMLzOyRm7HDmPQ1XpJgtbcslmKZGoZzVQmwwV1x1McBt; logged_in=yes; dotcom_"
          "user=yandifei; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%"
          "7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%"
          "3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg;"
          " preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=hTmjbvhWFNyNfnWOnOrzwRExAb"
          "3oGmgU5GQEiCD3R%2FeWklQApZQGtIAR9HhXyxzzjpxYny4Ujd9q6r%2BuQvteGDiqidNXP%2B6rZcmEjO7A"
          "riAJQVM10fKOW5CibuwFeZ6V%2FBhGdEHzeY%2Fo7%2B4Z0mxi%2F6BMYIyLYXancSnMEhi1zWVyLKlm74tM"
          "naSAVKyyLsdSb0h1S3xoOcwqyC5glE%2FMEotGGEVh0JsRdFtqpuw6Huox3cP4u81uds9doAV%2FO1VHA7t"
          "zuSHbRgFiB0lY60r7EK%2Bvh7ckZRq2Rluevy%2BxVVE9UeK9u6UL8AjIDJY3XyIxfWbXhzuhjoCm86gKOYl"
          "gepk%2FlJGp%2BrzPRCR3meWyg5Tgc6muP15JNbkEKA314nro--kbIfVLWTjjbB%2Fivh--911UmozPr7qRX"
          "TYDkFHxZg%3D%3D")

# 先分割"; "后再替换"="为":"，最后转为字典
cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in Cookie.split("; ")}
print(cookies)

# 构建请求（verify直接禁用）
response = requests.get(url, headers=headers, cookies=cookies, verify=False)

# 以二进制的形式写入html文件
with open("github_cookies2.html", "wb") as f:
    f.write(response.content)   # 把内容写入进去