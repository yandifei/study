"""
requests模块发送post请求
思考：哪些地方我们会用到POST请求?
1.登录注册（在web工程师看来POST比GET更安全，urI地址中不会暴露用户的账
号密码等信息）
2.需要传输大文本内容的时候（POST请求对数据长度没有要求）
所以同样的，我们的爬虫也需要在这两个地方回去模拟浏览器发送post请求
"""
import requests
import json # 用来数据解析
# 发送post请求一般附带data的参数(字典)。get参数可以直接搬过来
# response = requests.post(url, data)

class Translation:
    def __init__(self, word):
        # self.url = "https://www.iciba.com/translate" # 金山翻译(其实现在已经加密了)
        self.url = "http://fy.iciba.com/ajax.php?a=fy"  # 视频里面的链接
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
        }
        self.data = {
            "from": "auto",
            "to": "auto",
            "q": word
        }

    def get_data(self):
        """#使用post方法发送个post请求，data为请求体的字典"""
        response = requests.post(self.url, data=self.data, headers=self.headers)
        return response.content.decode()

    def parse_data(self, data):
        """解析数据"""
        # loads方法将json字符串转换成python字典
        dict_data = json.loads(data)

        print(dict_data["content"]["out"])


    def run(self):
        # 编写爬虫逻辑

        # url
        # headers 伪装
        # data字典
        # 发送请求获取响应
        # 数据解析
        response = self.get_data()
        print(response)
        # 数据解析
        self.parse_data(response)

if __name__ == '__main__':
    # word = input("请输入要翻译的单词或句子")
    import sys
    word = sys.argv[1] # 接收终端第二个参数
    translation = Translation("字典")
    translation.run()       # 这里使用必报错，已经不是当年的了，有加密

"""
requests模块发送post请求
    1.实现方法
    requests.post(url, data)
    data是一个字典
2.post数据来源
    1.固定值               抓包比较不变值
    2.输入值               抓包比较根据自身变化值
    3.预设值-静态文件          需要提前从html中分析
    4.预设值-发请求           需要对指定地址发送请求
    5.在客户端生成的           分析js，模拟生成数据
"""