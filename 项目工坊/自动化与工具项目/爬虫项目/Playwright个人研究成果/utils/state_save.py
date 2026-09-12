"""state_save.py
保存浏览器的用户数据并复用
cookies + localStorage + 可选 IndexedDB
"""
# 内置库
import threading
from pathlib import Path
# 三方库
# from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext

from utils import info


class StateSaving:
    _instance = None  # 单例实例
    _lock = threading.Lock()  # 线程锁，确保线程安全

    def __new__(cls):
        """确保创建为单例:线程安全双重检查锁定 (DCL)
        :return: 单例实例
        """
        # 第一次检查：如果实例不存在，进入同步块
        if cls._instance is None:
            # 获取锁，确保只有一个线程进行实例化
            with cls._lock:
                # 第二次检查：避免在等待锁的过程中，实例已经被其他线程创建
                if cls._instance is None:
                    # 进行实例化操作
                    cls._instance = super().__new__(cls)

    def __init__(self):
        info("StateSaving 单例化完成")

    @staticmethod
    def save_browser_status(context : BrowserContext, save_path: str | Path):
        """保存用户数据
        :param context: 浏览器上下文
        :param save_path: 状态文件保存路径（必须是完整的文件路径，如: 'user_data/chrome_data/state.json'）
        :return:
        """
        file_path = Path(save_path)

        # 确保保存文件的父目录存在
        if not file_path.parent.exists():
            # 使用 parents=True 确保递归创建所有缺失的父目录
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # indexed_db=True 确保 IndexedDB 数据也被包含
        context.storage_state(path=file_path, indexed_db=True)

        # 返回保存的文件路径
        return file_path

if __name__ == '__main__':
    # a = StateSaving()
    # a.save_browser_status()
    StateSaving.save_browser_status()
