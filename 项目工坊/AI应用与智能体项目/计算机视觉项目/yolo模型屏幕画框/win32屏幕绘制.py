import win32gui, win32con, win32api


def fast_draw_rect(x1, y1, x2, y2):
    # 获取桌面窗口的上下文 (HDC)
    hwnd = win32gui.GetDesktopWindow()
    hdc = win32gui.GetWindowDC(hwnd)

    # 创建一个画笔 (绿色, 2像素宽)
    pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(0, 255, 0))
    old_pen = win32gui.SelectObject(hdc, pen)

    # 设置透明背景，防止文字遮挡
    win32gui.SetBkMode(hdc, win32con.TRANSPARENT)

    # 绘制矩形 (GDI 绘图速度极快)
    win32gui.Rectangle(hdc, x1, y1, x2, y2)

    # 清理资源 (必须清理，否则会造成 GDI 泄露导致系统卡顿)
    win32gui.SelectObject(hdc, old_pen)
    win32gui.DeleteObject(pen)
    win32gui.ReleaseDC(hwnd, hdc)

while True:
    fast_draw_rect(100, 100, 100, 100)
    fast_draw_rect(10, 10, 100, 100)
