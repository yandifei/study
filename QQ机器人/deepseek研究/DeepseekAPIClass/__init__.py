import os   # 导入系统库
# 从环境变量获取密钥
try:
    DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']   # 从环境变量读取deepseek的api密钥
except KeyError:
    raise KeyError(f"未在环境变量中找到deepseek的api密钥，请确保添加成功，如果确认已经添加请重启pycharm或该程序")
import requests

# 测试请求到模型列表端点
response = requests.get(
    "https://api.deepseek.com/user/balance",   # 请求网址
    headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"} # 请求头
)
if response.status_code != 200: # 检查响应状态码
    raise ValueError ("API密钥无效或未授权，检查密钥是否正确或重启pycharm或程序")
