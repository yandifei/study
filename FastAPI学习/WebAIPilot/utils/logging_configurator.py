"""logging_configurator.py
日志配置器
解析日志配置文件，确保系统初始化的时候就能加载日志记录器
"""
# 内置库
import threading
from pathlib import Path
from typing import Tuple
# 第三方库
import yaml
from yaml.scanner import ScannerError
# 自己的模块
from utils.path_utils import is_path_exist, get_root, mkdir

"""日志路径相关
先加载默认硬编码配置，如果配置文件无法解析就检查日志输出路径是否存在
如果不存在就创建这个日志输出路径
最后抛出致命错误写入日志文件和输出到控制台
"""
def is_logs_outputs_path_exist(path: str | Path, depth: int = 2) -> Path | bool:
    """检查指定路径下是否存在 outputs/logs 目录

    在指定的目录层级范围内查找 logs 目录，默认向上搜索2层。

    :param path: 基准路径
    :param depth: 向上搜索的深度，默认为2层
    :return: 如果找到 logs 目录返回路径，否则返回 False
    """
    # 检查当前路径下的 outputs/logs
    if is_path_exist(logs_path := Path(path) / "outputs" / "logs"):
        return logs_path

    # 向上搜索指定层级
    logs_path = Path(path)
    # 层级减1
    for _ in range(depth):
        logs_path = logs_path.parent
        # 如果路径存在就退出
        if is_path_exist(logs_path / "outputs" / "logs"):
            return logs_path

    return False

def create_logs_path() -> Path:
    """在项目目录下创建日志输出路径 "./outputs/logs"
    :return: 日志输出的绝对路径（项目根路径/outputs/log）
    """
    # 在根目录下创建 outputs/logs 目录
    mkdir(logs_dir := get_root() / "outputs" / "logs")
    return logs_dir

class LoggingConfigurator:
    """日志配置器"""
    # 存储单例实例的类变量
    _instance = None
    # 是否已经实例化了(避免重复初始化)
    _initialized = False
    # 类级锁，确保多线程环境下的线程安全
    _lock = threading.Lock()

    def __new__(cls):
        """确保创建为单例:线程安全双重检查锁定 (DCL)"""
        # 如果实例已经存在，直接返回
        if cls._instance is None:
            # 获取锁，确保只有一个线程进行实例化
            with cls._lock:
                # 避免在等待锁的过程中，实例已经被其他线程创建
                if cls._instance is None:
                    # 进行实例化操作
                    cls._instance = super().__new__(cls)
        # 返回单例
        return cls._instance

    def __init__(self):
        # 确保配置只加载一次
        if not hasattr(self, '_initialized'):
            # 设置被初始化的标志位
            self._initialized = True
            # 记录错误信息
            self.error_msg : Tuple[str | None, Exception | None]= (None, None)
            # 初始化配置数据(字典)

    """加载日志配置"""
    def load_logging_config(self, path: str | Path) -> dict | bool:
        """加载日志配置
        解析错误就去error_msg找错误信息
        :param path: 日志配置文件的路径
        :return: 如果路径和配置正确则返回 解析字典，否则返回 False
        """
        # 检查文件是否存在
        if not Path(path).is_file():
            self.error_msg = (f"日志配置文件不存在：{path}", FileNotFoundError(path))
            return False
        # 检查文件配置是否正确
        try:
            with open(path, 'r', encoding='utf-8') as file:
                # 尝试安全加载文件内容。如果语法有问题，会抛出异常。
                return yaml.safe_load(file)
            # 如果加载成功，则认为格式正确
            # del self.error_msg  # 销毁这个没用的对象（方法得要复用不能销毁）
        except ScannerError as e:
            # ScannerError 专门捕获语法错误
            self.error_msg = f"日志配置文件语法错误（{path}）", e
            # print(e)
            return False
        except yaml.YAMLError as e:
            # 其他 YAML 错误，如解析错误
            self.error_msg = f"日志配置文件解析错误（{path}）", e
            # print(e)
            return False
        except Exception as e:
            # 捕获其他文件操作错误（如文件不存在、被加权限了）
            self.error_msg = f"日志配置文件操作错误（{path}）", e
            # print(e)
            return False

    # @staticmethod
    # def is_global_config_exist(path: str | Path, depth: int = 2) -> Path | bool:
    #     """检查全局配置是否存在
    #
    #     在指定的目录层级范围内查找 config 目录，默认向上搜索2层。
    #
    #     :param path: 基准路径
    #     :param depth: 向上搜索的深度，默认为2层
    #     :return: 如果找到 logs 目录返回路径，否则返回 False
    #     """
    #     # 检查当前路径下的 outputs/logs
    #     if is_path_exist(logs_path := Path(path) / "config"):
    #         return logs_path
    #
    #     # 向上搜索指定层级
    #     logs_path = Path(path)
    #     # 层级减1
    #     for _ in range(depth):
    #         logs_path = logs_path.parent
    #         # 如果路径存在就退出
    #         if is_path_exist(logs_path / "config"):
    #             return logs_path
    #
    #     return False




if __name__ == '__main__':
    logging_configurator = LoggingConfigurator()
    if json := logging_configurator.load_logging_config("../user_data/logging_config.yaml"):
        print(json)
    else:
        if not is_logs_outputs_path_exist("outputs/logs/日志记录.log"):
            # 创建日志输出目录和创建日志文件
            (create_logs_path() / "error.log").touch(exist_ok=True)
        print(logging_configurator.error_msg[0])
        print(logging_configurator.error_msg[1])