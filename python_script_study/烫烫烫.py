# 构造连续的0xCC字节（偶数个）
data = b'\xCC' * 20  # 20字节10组0xCCCC
# 使用GBK解码生成字符串
try:
    result = data.decode('gbk')
except UnicodeDecodeError:  # 处理可能的解码错误（如奇数字节时）
    result = data.decode('gbk', errors='replace')

print(result)