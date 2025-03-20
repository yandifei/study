# 简单应用题
# 34



class Exercise:
    def __init__(self):
        pass
    def turtle_34(self):
        import turtle
        # for i in range(3):
        turtle.fd(200)
        turtle.seth(120)
        turtle.fd(200)
        turtle.seth(-120)
        turtle.fd(200)
        turtle.done()

    # @staticmethod
    def score35(self):
        score = {"数学": 101, "语文": 202, "英语": 203, "物理": 204, "生物": 206}
        print(score)
        score["化学"] = 205
        print(score)
        score["数学"] = 201
        print(score)
        score.pop("生物")
        print(score)


# a  = Exercise()
# a.turtle_34()
# a.score35()


# earth_weigh = 0.5 * 10 # 十年增长的重量
# moon_weigh = earth_weigh * 0.165
# print(f"地球的体重是{earth_weigh}kg ,月球的体重是{moon_weigh}kg")
# a = "105C"
# print(a[0:-2])
# print(1.23e-4+5.67e+8j.real)
# s = 'PYTHON'
# print("{0:3}".format(s))
# print("<'a')

a,b = 0, 1
while a <= 100:
    print(a,end=',')
    a,b = b, a+b    # 给出具体解释
