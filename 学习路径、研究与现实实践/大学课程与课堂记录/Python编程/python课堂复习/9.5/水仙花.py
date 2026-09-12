"""水仙花的定义
一个三位数，它的各位数字的立方和等于它本身。
"""
num = int(input("num:"))
if 99 < num < 100:
    bai = num // 100
    shi = num // 10 % 10
    ge = num % 10
    if  bai**3 + shi **3 + ge**3 == num:
        print("{}水仙花数".format(num))
    else:
        print("{}不是水仙花数".format(num))
else:
    print("请输入正确的三位数")
