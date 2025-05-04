import win32gui
import win32api
import win32con


def send_key(hwnd, key_code, is_extended=False):
    """
    发送单个按键到指定窗口
    :param hwnd: 目标窗口句柄
    :param key_code: 虚拟键码（如 win32con.VK_A）
    :param is_extended: 是否是扩展键（如方向键）
    """
    # 构造扩展标志(允许使用小键盘区Home键等)
    ext_flag = 0x0001 if is_extended else 0
    # 发送按下消息
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, key_code, ext_flag)
    # 发送抬起消息
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, key_code, ext_flag | 0xC0000000)


# 使用示例：发送回车键
send_key(10160218, 0x30)