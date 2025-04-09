"""这个库用来监控QQ消息，监控Q群成员的消息，以及监听QQ好友的消息
内置判断是Q群还是QQ好友
"""
import uiautomation

class QQMessageMonitor:
    def __init__(self):
        return


if __name__ == '__main__':
    root_win = uiautomation.GetRootControl()
    root_win.GetChildren()
