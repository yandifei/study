# 导入包
import threading    # 线程的包
import time     # 导入时间相关的包
from time import sleep


def sing(a):
    while True:
        print(a)
        time.sleep(1)

def dance(b):
    while True:
        print(b)
        time.sleep(1)

if __name__ == '__main__':
    # 创建线程
    sing_thread = threading.Thread(target=sing, args=("唱歌",))   # 元组传参
    dance_thread = threading.Thread(target=dance, kwargs={"b": "跳舞"})   # 字典传参
    # 启动线程
    sing_thread.start()
    dance_thread.start()
    # 主进程停止3秒
    sleep(3)
    print("主进程已经结束了")
    """
    实验结果表明，即使主进程结束了，线程依旧还在工作
    """



