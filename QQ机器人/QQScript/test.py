import uiautomation as auto
import win32gui
import win32con
# [1705496, 197892, 3081948]
win32gui.ShowWindow(1705496, win32con.SW_MAXIMIZE)
def get_qq_win_hwnd():
    """判断登录了多少个QQ   1. 把符合句柄的窗口展示出来 2. 通过结构判断是不是qq窗口
    返回值： qq_win_hwnd : qq窗口句柄的列表
    """
    suspected_qq_hwnd = list()  # 疑似qq窗口句柄
    def enum_child(hwnd, _):  # 回调函数
        # if not win32gui.IsWindowVisible(hwnd):  # 过滤不可见的窗口
        #     return True  # 直接跳过
        if win32gui.GetClassName(hwnd) == "Chrome_WidgetWin_1" and win32gui.GetWindowText(hwnd) == "QQ":
            suspected_qq_hwnd.append(hwnd)  # 获得所有的qq类名和标题的句柄
        return True  # 继续遍历
    win32gui.EnumChildWindows(None, enum_child, None)  # 遍历函数
    print(suspected_qq_hwnd)
    """结构判断"""
    qq_win_hwnd = list()  # 放置QQ号窗口句柄
    # 遍历疑似qq窗口的句柄
    visible_windows = uiautomation.GetRootControl().GetChildren()  # 获取当前桌面对象->获得当前桌面所有可见的窗口的对象
    for qq_hwnd in suspected_qq_hwnd:   # 遍历符合类名和标题的窗口句柄
        win32gui.SetWindowPos(qq_hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)  # 窗口置顶
        for visible_window in visible_windows:
            if visible_window.NativeWindowHandle != qq_hwnd:   # 遍历是否qq的句柄
                continue   # 如果不符合就跳过此次循环
            if visible_window.GetChildren()[0].LocalizedControlType != "文档":  # 报错警告（没有文档对象）
                raise EnvironmentError("请手动把QQ窗口显示在桌面上")
                # 通过结构判断是QQ窗口还是对话窗口
            # 如果是QQ号则为4，对话窗口为1
            if len(visible_window.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()) == 4:
                qq_win_hwnd.append(qq_hwnd)  # 把十进制的qq窗口句柄放置在列表种
            break   # 跳出循环
        win32gui.SetWindowPos(qq_hwnd, win32con.HWND_NOTOPMOST,
                              0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)  # 取消置顶
    return qq_win_hwnd