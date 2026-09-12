# 基于 tkinter模块创建 GUI程序包含如下4个核心步骤
# 1.创建应用程序主窗口对象(也称:根窗口)
from tkinter import *
from tkinter import messagebox
# 创建窗口对象
root = Tk()


button1 = Button(root)
button1["text"] = "点击我送花"
button1.pack() # 调用布局关系
def songhua(e):     # e就是事件对象
    messagebox.showinfo("Message", "送你一朵玫瑰花")
    print("送你99朵玫瑰花")

# 事件绑定
button1.bind("<Button-1>", songhua)

root.mainloop()  # 调用组件的mainloqp()方法，进入事件循环


