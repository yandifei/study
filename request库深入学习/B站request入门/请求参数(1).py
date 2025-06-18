"""
# 百度搜索python后的url
"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=python&fenlei=256&rsv_pq=0x9113dfd8007e1fb3&rsv_t=69f0BwBjxJgiAPftmyJVGPWCCtg328aevXw17mapWKtkd5KPGxyNVulGH7d1&rqlang=en&rsv_dl=tb&rsv_enter=1&rsv_sug3=7&rsv_sug1=6&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=2079&rsv_sug4=2900"
"https://www.baidu.com/s?&wd=python"    # 从上面的url不断尝试删去参数后发现这个网页依旧不变，显示结果和上卖一样
"""
import requests
# url = "https://www.baidu.com/s?&wd=python"
# # 带上请求头
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
#
# }
# # 构建请求
# response = requests.get(url, headers=headers)   # 如果不加请求头就拿不到完整的数据
#
# # 写入保存
# with open("baidu.html", "wb") as f:  # 二进制写入
#     f.write(response.content)   # 把二进制内容写入html文件里面去


# url = "https://www.baidu.com/s?&wd=python"    # 这是带参数的请求
url = "https://www.baidu.com/s?"      # 这时不带参数的请求
# 带上请求头
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"

}

# 构建参数字典
params = {
    "wd": "python"
}

# 构建请求
response = requests.get(url, headers=headers, params=params)   # 如果不加请求头就拿不到完整的数据

# 打印带参数的后请求的url
print(response.url)
# 写入保存
with open("baidu1.html", "wb") as f:  # 二进制写入
    f.write(response.content)   # 把二进制内容写入html文件里面去