import requests

def get_city_info():
    # 接口地址
    url = "https://iploc.ywdier.com/api/iploc5/search/city"

    try:
        # 发送 GET 请求
        response = requests.get(url, timeout=10)

        # 检查 HTTP 状态码
        response.raise_for_status()

        # 解析返回的 JSON 数据
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None


# 测试调用
if __name__ == "__main__":
    result = get_city_info()

    if result:
        print("接口返回数据内容：")
        print(result)
    else:
        print("未能获取到数据。")