from time import sleep

from phone import Phone
p  = Phone()
while True:
    num = int(input("请输入手机号："))
    print(p.find(num))
