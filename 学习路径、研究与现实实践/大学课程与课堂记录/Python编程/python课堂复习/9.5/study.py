

# 以前没注意的细节
"""缩进会影响多行字符串的构建"""
def a():
    text = """1
fdfsd
sdfdsf
    """
    print(text)

a()

"""
字符串构建可以用占位符
"""
print("hello w%s" % "orld")
print("你好，我叫%s，今年%d岁"%("小明",18))
print("我的名字是{}".format("yandifei"))
print("我的名字是{0},今年{1}岁".format("yandifei", 15))
print("我的名字是{1},今年{0}岁".format("yandifei", 15))