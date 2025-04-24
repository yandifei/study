import requests

url = "https://api.deepseek.com/user/balance"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '  #
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(type(response.text))  # 返回的是str类型
# 开始解析(必须使用json库，本身就是文本格式和避免陷阱)
import json
data = json.loads(response.text)  # 解析json数据

if data["is_available"]:  # 如果为True
  print("余额充足，api可以调用")
elif not data["is_available"]:  # 如果为False
  print("余额不足，api无法调用")

detail_list = data["balance_infos"] # 详细信息

# currency_type =
if detail_list[0]["currency"] == "CNY":   # 人民币
  print("货币类型为人民币")
elif detail_list[0]["currency"] == "USD":   # 美元
  print("货币类型为美元")

print(f'总的可用余额(包括赠金和充值余额):{detail_list[0]["total_balance"]}')
print(f"未过期的赠金余额:{detail_list[0]["granted_balance"]}")
print(f"充值余额:{detail_list[0]["topped_up_balance"]}")

# 返回格式
# {
#   "is_available": true,   # 当前账户是否有余额可供 API 调用
#   "balance_infos": [
#     {
#       "currency": "CNY",  # 货币，人民币或美元CNY, USD
#       "total_balance": "110.00",  # 总的可用余额，包括赠金和充值余额
#       "granted_balance": "10.00", # 未过期的赠金余额
#       "topped_up_balance": "100.00"   # 充值余额
#     }
#   ]
# }

"""数值计算"""
# 1 个英文字符 ≈ 0.3 个 token。1 个中文字符 ≈ 0.6 个 token。
# R1 保底模型字数计算
# 16÷1000000 = 62500(元/tokens)  16元除以一百万
min_token = float(detail_list[0]["total_balance"]) * 62500 # 当前金额(元) * 62500[每元的token数]
characters = int(min_token / 0.6)   # 最少的中文字符字数(直接取整数)
words = int(min_token / 0.3)    # 最少的英文字符字数(直接取整数)
print(f"当前可用余额能生成最少 {int(min_token)} token，对话可使用最少约{characters}个汉字，对哈可使用最少约{words}英文字符")