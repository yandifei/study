import requests

proxies = {
    "https": "106.75.251.211:3128"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
}

response = requests.get("https://baidu.com", headers=headers, proxies=proxies)
print(response)