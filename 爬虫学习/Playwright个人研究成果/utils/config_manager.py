"""config_manager.py
给我统一管理配置文件读取
当然，这么多配置文件有些还只用一次所以还是想省内存的（配置管理）
企业级的做法：配置单例化（Singleton Configuration）+ 依赖注入（Dependency Injection, DI）
"""
# 内置库
import threading
from pathlib import Path
from typing import Dict, Any
# 第三方库
import yaml
# 自己的模块
from utils.logging_configurator import LoggingConfigurator, create_logs_path
from utils.path_utils import get_root


class ConfigManager:
    # 存储单例实例的类变量
    _instance = None
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
        # 确保配置只加载一次(Pythonic写法)
        if not hasattr(self, '_initialized'):
            # 设置被初始化的标志位
            self._initialized = True
            # 初始化配置数据(字典)
            self.config_data = {}
            # 日志配制器
            self.logging_configurator = LoggingConfigurator()
            # 加载所有配置文件（拿到标志位）
            self.success_flag = self.load_config()


    def load_config(self) -> Dict[str, Any] | bool:
        """加载所有配置文件(会进行层叠覆盖)
        日志置加载失败返回False，其他直接抛出异常，如果配置加载成功返回字典

        :return:配置有效且层叠成功返回True否则返回False
        """

        # 框架默认日志配置(日志配置错误就没必要加载后面的了)
        if self.load_logging_config() is False:
            return False
        # 用户私有日志配置(日志配置错误就没必要加载后面的了)
        if self.load_user_logging_config() is False:
            return False
        # 框架默认设置配置

        # 用户私有设置配置

        # 最后返回配置数据
        return True

    def load_logging_config(self) -> Dict[str, Any] | bool:
        """加载默认的日志配置并进行覆盖"""
        # 检查日志配置文件是否存在
        if not Path(get_root() / "config" / "logging_config.yaml").exists():
            # # 确保日志输出目录和日志文件存在（打印和记录全局配置文件丢失的错误）
            # (create_logs_path() / "error.log").touch(exist_ok=True)
            # (create_logs_path() / "日志记录.log").touch(exist_ok=True)
            return False  # 直接返回False
        # 加载全局的日志配置
        if json := self.logging_configurator.load_logging_config(get_root() / "config" / "logging_config.yaml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        # # 确保日志输出目录和日志文件存在（打印和记录全局配置文件丢失的错误）
        # (create_logs_path() / "error.log").touch(exist_ok=True)
        # (create_logs_path() / "日志记录.log").touch(exist_ok=True)
        return False  # 直接返回False

    def load_user_logging_config(self) -> Dict[str, Any] | bool:
        """加载用户的日志配置并进行覆盖"""
        # 检查用户的日志配置文件是否存在
        if not Path(get_root() / "user_data" / "logging_config.yaml").exists():
            # # 确保日志输出目录和日志文件存在（打印和记录全局配置文件丢失的错误）
            # (create_logs_path() / "error.log").touch(exist_ok=True)
            # (create_logs_path() / "日志记录.log").touch(exist_ok=True)
            return False  # 直接返回False
        # 加载用户的日志配置
        if json := self.logging_configurator.load_logging_config(get_root() / "user_data" / "logging_config.yaml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        # # 确保日志输出目录和日志文件存在（打印和记录全局配置文件丢失的错误）
        # (create_logs_path() / "error.log").touch(exist_ok=True)
        # (create_logs_path() / "日志记录.log").touch(exist_ok=True)
        return False  # 直接返回False


    @staticmethod
    def load_yaml(path: Path) -> Dict[str, Any]:
        """
        加载YAML配置文件并将其解析为Python字典，使用UTF-8编码读取文件
        :param path: 配置文件的路径对象，必须是Path类型
        :return: 解析后的配置字典，如果文件为空则返回空字典
        :raises FileNotFoundError: 当指定的配置文件不存在时抛出此异常
        """
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {path}")
        with path.open("r", encoding="utf-8") as yaml_file:
            config_data = yaml.safe_load(yaml_file) or {}
        return config_data

    def deep_merge(self, base: dict, override: dict) -> dict:
        """配置深度合并：override 覆盖 base，但保持 base 原有结构不被破坏"""
        for key, value in override.items():
            if (
                    key in base
                    and isinstance(base[key], dict)
                    and isinstance(value, dict)
            ):
                self.deep_merge(base[key], value)
            else:
                base[key] = value
        return base


if __name__ == '__main__':
    cm = ConfigManager()
    data = cm.load_yaml(Path(r"/config/logging_config.yaml"))
    print(data)
