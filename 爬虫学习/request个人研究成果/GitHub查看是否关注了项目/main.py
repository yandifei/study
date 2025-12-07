import requests

url = "https://github.com/yandifei/ArisuQQChatAI/stargazers?="

query_user = "1"

headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}
params = {

}
data = {
    "name": "ChatGPT",
    "type": "demo",
    "active": True
}
https://api.github.com/users/yandifei/starred/zhiyiYo/PyQt-Fluent-Widgets
response = requests.post(
    url=url.join(query_user),
    headers=headers,
    params=params,
    json=data,
    timeout=10
)
print(response.status_code)