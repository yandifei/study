"""Balance inquiry(余额查询)
查询deepseek的api余额
计算还能用多少token数，交流的字数(默认utf8-3字节一个字)
"""
import requests # 导入网络请求的库
import json

def balance_inquiry(DEEPSEEK_API_KEY):
  """查询deepseek的API余额
  参数：DEEPSEEK_API_KEY ： API密钥
  返回值：返回一个列表
  0 ： 布尔值（余额是否充足）
  1 ： 字符串型（货币类型）
  2 : 字符串型（总的可用余额(包括赠金和充值余额)）
  3 ： 未过期的赠金余额
  4 ： 充值余额
  """
  return_list = list()  # 返回值的列表
  url = "https://api.deepseek.com/user/balance" # 余额查询网址
  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {DEEPSEEK_API_KEY}'  # 密钥
  }
  response = requests.request("GET", url, headers=headers, data=payload)  # 发送查询请求
  data = json.loads(response.text)  # 解析json数据，(必须使用json库，本身就是文本格式和避免陷阱)
  if data["is_available"]:  # 如果为True
    return_list.append(True)
    print("\033[92m余额充足，api可以调用\033[0m",end="\t")
  elif not data["is_available"]:  # 如果为False
    return_list.append(False)
    print("\033[91m余额不足，api无法调用\033[0m",end="\t")
  detail_list = data["balance_infos"] # 详细信息
  currency_type = ""  # 货币类型放置
  if detail_list[0]["currency"] == "CNY":   # 人民币
    return_list.append("元")
    currency_type = "元" # 货币类型为人民币
  elif detail_list[0]["currency"] == "USD":   # 美元
    return_list.append("美元")
    currency_type = "美元"  # 货币类型为美元
  return_list.append(detail_list[0]["total_balance"])
  return_list.append(detail_list[0]["granted_balance"])
  return_list.append(detail_list[0]["topped_up_balance"])
  print(f"总的可用余额(包括赠金和充值余额):{detail_list[0]["total_balance"]}{currency_type}",end="\t")
  print(f"未过期的赠金余额:{detail_list[0]["granted_balance"]}{currency_type}",end="\t")
  print(f"充值余额:{detail_list[0]["topped_up_balance"]}{currency_type}")

def token_(DEEPSEEK_API_KEY):
  """数值计算
  参数：DEEPSEEK_API_KEY ： API密钥
  返回值：返回一个列表
  min_token : 可用token数
  characters ： 最少的中文字符字数(直接取整数)
  words ： 最少的英文字符字数(直接取整数)
  round(((characters*24)/1024)/1024,2)  ： 最少可生产的数据(GB)
  round(characters/880000,2)  : 约几本《三体》(88万字一本)
  """
  url = "https://api.deepseek.com/user/balance"  # 余额查询网址
  payload = {}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {DEEPSEEK_API_KEY}'  # 密钥
  }
  response = requests.request("GET", url, headers=headers, data=payload)  # 发送查询请求
  data = json.loads(response.text)  # 解析json数据，(必须使用json库，本身就是文本格式和避免陷阱)
  detail_list = data["balance_infos"]  # 详细信息
  min_token = float(detail_list[0]["total_balance"]) * 62500 # 当前金额(元) * 62500[每元的token数]
  characters = int(min_token / 0.6)   # 最少的中文字符字数(直接取整数)
  words = int(min_token / 0.3)    # 最少的英文字符字数(直接取整数)
  print(f"当前可用余额能生成最少 {int(min_token)} token，对话可使用最少约{characters}个汉字，对话可使用最少约{words}英文字符")
  print(f"最少可生产:{round(((characters*24)/1024)/1024,2)}GB 的对话数据， 约{round(characters/880000,2)}本《三体》(88万字一本)")
  return min_token, characters, words, round(((characters*24)/1024)/1024,2), round(characters/880000,2)

if __name__ == '__main__':
  balance_inquiry("sk-d5da84db73394e29bc3ce3aab5c9e474")
