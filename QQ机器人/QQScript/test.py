import uiautomation as auto

print("成功导入uiautomation")
# ->窗口
win = auto.GetRootControl()
##print(win)
win_childs = win.GetChildren()    # 获得根窗口
##qq_win = 0
print(win.Next())