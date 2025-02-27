
# 接受传入字符串，将字符串反转返回
def str_reverse(s):
    return s[::-1]

# 按照下标x和y，对字符串进行切片
def substr(s,x,y):
    return s[x:y]

if __name__ == '__main__':
    a = str_reverse("asdfas")
    print(a)
    a = substr("asdfas", 1, 3)
    print(a)