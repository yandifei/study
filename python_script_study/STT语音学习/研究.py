from time import sleep

import pyttsx3

# 官方例子
engine = pyttsx3.init()
engine.startLoop(False) # 非阻塞启动循环

while True:
    engine.say("1")
    # 需要手动驱动引擎迭代，并添加延迟或其他操作
    while engine.isBusy(): # 检查引擎是否繁忙
        engine.iterate()
        sleep(0.1) # 避免CPU占用过高



