# 计算三角形的面积

"""
使用海伦公式
"""
jude = lambda a, b, c: (a + b) > c and (a + c) > b and (b + c) > a

def length(x, y ,z):
    if jude(y, z, x):
        p = (x + y + z) / 2
        # 海伦公式（这里是0.5次幂来代表开根号，我是真没想到）
        return (p * (p - x) * (p - y) * (p - z)) ** 0.5
    return "不符合三角形的定义（两边之和大于第三边）"

recode = lambda prompt : int(input("请输入三角形的" + prompt + ":"))
print(length(recode("x"), recode("y"), recode("z")))