import requests

with open("图片.png", 'wb') as f: f.write(requests.post("http://www.dmoe.cc/random.php").content)