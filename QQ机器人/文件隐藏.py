
def hide_win(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)  # 隐藏

def show_win(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # 隐藏