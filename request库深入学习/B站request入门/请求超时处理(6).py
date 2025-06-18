import requests


url = "https://twitter.com"     # 推特官网，国内访问不上
# 参数 timeout 是请求等待的意思，默认None，无限等待
# 一定要设置等待超时 timeout 的参数，不然对面卡住你就会一直等待
requests = requests.get(url,timeout=3)