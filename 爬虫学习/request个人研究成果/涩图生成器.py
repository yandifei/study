import requests # 爬虫库
from datetime import datetime # 时间命名
from PIL import Image   # webp转为png
from io import BytesIO  # 二进制数据处理

# 声明
notice = """
作者：雁低飞
作者Github主页：https://github.com/yandifei
本程序没有使用任何协议，只有一个要求：禁止使用在非法领域。
"""

# url = "https://t.alcy.cc/moe" # 二次元萌图
# url = "https://v2.xxapi.cn/api/baisi?return=302"    # 三次元白丝
url = "https://v2.xxapi.cn/api/heisi?return=302"    # 三次元黑丝
r = requests.get(url,timeout=60)    # 1分钟超时

# print(r.content)
# 开始写入webp的图片文件
# with open(f"{image_name}.webp", "wb") as image:
#     image.write(r.content)
try:
    with Image.open(BytesIO(r.content)) as img:
        # 转换为RGB模式（确保兼容性）
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 文件名字以当前时间命名
        image_name = f"{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.png"
        # 保存为PNG格式
        img.save(image_name, "PNG")
except requests.exceptions.RequestException as e:
    print(f"网络请求失败: {str(e)}")
except Exception as e:
    print(f"处理图片时出错: {str(e)}")
