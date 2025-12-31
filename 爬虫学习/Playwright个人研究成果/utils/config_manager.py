"""config_manager.py
给我统一管理配置文件读取
当然，这么多配置文件有些还只用一次所以还是想省内存的（配置管理）
企业级的做法：配置单例化（Singleton Configuration）+ 依赖注入（Dependency Injection, DI）
"""
# 内置库
import threading
import tomllib
from pathlib import Path
from typing import Dict, Any, Tuple
# 第三方库
import yaml
# 自己的模块
from utils.logging_configurator import LoggingConfigurator
from utils.path_utils import get_root
from utils.logger import logger_manager, error
from utils.playwright_factory.context_options import ContextOptions
from utils.playwright_factory.launch_options import LaunchOptions


class ConfigManager:
    # 存储单例实例的类变量
    _instance = None
    # 类级锁，确保多线程环境下的线程安全
    _lock = threading.Lock()

    # 防止因为参数不匹配报错__init__报错
    def __new__(cls, *args, **kwargs):
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

    def __init__(self, debug: bool =  False):
        """初始化
        :param debug: 是否为debug模式，默认为false
        """
        # 确保配置只加载一次(Pythonic写法)
        if not hasattr(self, '_initialized'):
            # 设置被初始化的标志位
            self._initialized = True
            # 错误信息记录（非日志错误信息）
            self.error_msg: Tuple[str | None, Exception | None] = (None, None)
            # 是否为debug模式(开发模式，开始合并之前定义这个属性)
            self.debug: bool = debug
            # 初始化配置数据(字典)
            self.config_data = {}
            # 日志配制器
            self.logging_configurator = LoggingConfigurator()
            # 加载所有配置文件（拿到标志位）
            self.success_flag = self.load_config()


    def config_override(self):
        """配置覆盖
        :return: 覆盖成功返回True，覆盖失败返回False
        """
        # 覆盖日志配置(最底层的配置)
        logger_manager.use_logging_config(self)
        # 检查其他配置是否覆盖成功
        if self.success_flag is False:
            # 存在错误信息属性，抛出错误
            msg, exc = self.error_msg
            error(msg, exc_info=exc)
        return True

    def load_config(self) -> Dict[str, Any] | bool:
        """加载所有配置文件(会进行层叠覆盖)
        日志置加载失败返回False，其他直接抛出异常，如果配置加载成功返回字典

        :return:配置有效且层叠成功返回True否则返回False
        """

        # 框架默认日志配置(日志配置错误就没必要加载后面的了)
        if self.load_default_logging_config() is False:
            return False
        # 用户私有日志配置(日志配置错误就没必要加载后面的了)
        if self.load_user_logging_config() is False:
            return False
        # 框架默认设置配置
        if self.load_default_settings_config() is False:
            return False
        # 用户私有设置配置
        if self.load_user_settings_config() is False:
            return False
        # debug模型的设置配置(处于debug开启才触发合并)
        if self.debug and self.load_debug_settings_config() is False:
            return False
        # 配置校验和模型转化
        if not self.model_check_transformation():
            return False
        # 最后返回配置数据
        return True

    def load_default_logging_config(self) -> Dict[str, Any] | bool:
        """加载默认的日志配置并进行覆盖"""
        # 加载全局的日志配置(自动检查配置是否存在和有效)
        if json := self.logging_configurator.load_logging_config(get_root() / "config" / "logging_config.yaml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        return False  # 直接返回False

    def load_user_logging_config(self) -> Dict[str, Any] | bool:
        """加载用户的日志配置并进行覆盖"""
        # 加载用户的日志配置(自动检查配置是否存在和有效)
        if json := self.logging_configurator.load_logging_config(get_root() / "user_data" / "logging_config.yaml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        return False  # 直接返回False

    def load_default_settings_config(self) -> Dict[str, Any] | bool:
        """加载默认的设置配置并进行覆盖"""
        # 加载默认的设置配置(自动检查配置是否存在和有效)
        # if json := self.load_toml(get_root() / "config" / "user_settings.toml"):
        if json := self.load_toml(get_root() / "config" / "settings.toml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        return False  # 直接返回False

    def load_user_settings_config(self) -> Dict[str, Any] | bool:
        """加载用户的设置配置并进行覆盖"""
        # 加载用户的设置配置(自动检查配置是否存在和有效)
        if json := self.load_toml(get_root() / "user_data" / "user_settings.toml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        return False  # 直接返回False

    def load_debug_settings_config(self) -> Dict[str, Any] | bool:
        """加载开发的设置配置并进行覆盖"""
        # 加载开发的设置配置(自动检查配置是否存在和有效)
        if json := self.load_toml(get_root() / "debug_data" / "user_settings.toml"):
            # 进行层叠覆盖
            return self.deep_merge(self.config_data, json)
        # 配置存在错误(error_msg已经记录错误信息了)
        return False  # 直接返回False

    def model_check_transformation(self) -> bool:
        """配置校验和模型转化

        :return: 成功为True否则为false
        """
        try:
            # 将字典转换为模型对象(销毁原来的字典对象直接替换为模型)
            # print(self.config_data["playwright"]["launch_options"])
            self.config_data["playwright"]["launch_options"] = LaunchOptions(**self.config_data["playwright"]["launch_options"])
            # print(self.config_data["playwright"]["launch_options"])
            # print(self.config_data["playwright"]["context_options"])
            self.config_data["playwright"]["context_options"] = ContextOptions(**self.config_data["playwright"]["context_options"])
            # print(self.config_data["playwright"]["context_options"])
            return  True
        except Exception as e:
            self.error_msg = (f"配置文件转化模型错误: {e}", e)
            return False


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

    def load_toml(self, path: str | Path) -> dict | bool:
        """
        加载TOML配置文件并将其解析为Python字典，使用UTF-8编码读取文件
        :param path: 配置文件路径对象，必须是Path类型
        :return: 解析后的配置字典，如果文件为空则返回False
        """

        # 检查设置配置文件是否存在
        if not Path(path).exists():
            self.error_msg = (f"设置配置文件不存在:{path}", FileNotFoundError(path))
            return False
        # 检查文件配置是否正确
        try:
            with path.open("rb") as toml_file:
                # 如果加载成功，则认为格式正确
                return tomllib.load(toml_file)
        except tomllib.TOMLDecodeError as e:
            # 其内容不符合 TOML 格式规范时产生
            self.error_msg = f"设置配置文件语法错误:（{path}）", e
            return False
        except Exception as e:
            # 捕获其他文件操作错误（如文件不存在、被加权限了等等）
            self.error_msg = f"设置配置文件操作错误:（{path}）", e
            return False




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
