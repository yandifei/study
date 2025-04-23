import requests

url = "https://api.deepseek.com/user/balance"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer sk-12eaafd1ff2245b4ae038c02471984a7'  # "sk-12eaafd1ff2245b4ae038c02471984a7"
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