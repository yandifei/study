# 私有成员练习
class Phone:
    # 定义一个外部成员方法
    def call_by_5g(self):
        self.__check_5g()
        print("正在通话中")

    # 定义一个内部成员变量
    __is_5g_enable = False

    # 定义一个内部成员方法
    def __check_5g(self):
        if self.__is_5g_enable == True:
            print("5g开启")
        else:
            print("5g关闭，使用4g网络")

iphone = Phone()
iphone.call_by_5g()
