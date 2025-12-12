"""专门用于做日志记录处理，方便直接调用"""
# 系统库
import sys  # 系统库
import threading  # 线程库，用于线程锁
import logging  # 日志记录库
import logging.config   # 解析日志配置
from pathlib import Path
# from logging.handlers import RotatingFileHandler  # 日志大小轮转处理器
# from logging.handlers import TimedRotatingFileHandler  # 日志时间轮转处理器
# from sys import exc_info
from types import TracebackType
from typing import Mapping, Optional, Type, Tuple
# 第三方库
# import colorlog  # 颜色处理库
# 自己的模块
from utils import ConfigManager
from utils.logging_configurator import create_logs_path
from utils.path_utils import get_root, is_path_exist, mkdir  # 根路径导入
# from utils.logging_configurator import is_logs_path_exist, create_logs_path
# 全局名称
LOGGER_NAME = "WebAIPilot.py"   # 日志记录器名称


class LoggerManager:
    """日志管理器，单例模式"""
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
        # 返回单例
        return cls._instance

    def __init__(self):
        """初始化日志管理器
        初始化后默认使用的是写死的配置
        如果触发了崩溃异常日志文件是直接写到项目根目录下的（避免outputs/logs不存在导致无法写出日志文件）
        """
        # 确保配置只加载一次(Pythonic写法)
        if not hasattr(self, '_initialized'):
            # 设置实例化标志位
            self._initialized = True
            # 默认日志配置，硬编码
            self.default_config = {
                'version': 1,  # logging 配置版本号，固定为 1
                'disable_existing_loggers': False,  # 是否禁用已有的 logger，这里为 False 表示不禁用

                'formatters': {  # 定义日志格式
                    'verbose': {  # 详细格式
                        'format': '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(threadName)s - %(message)s',
                        # 日志输出格式：时间、级别、logger 名字、行号、线程名、消息
                        'datefmt': '%Y-%m-%d %H:%M:%S'  # 时间格式
                    },
                    'simple': {  # 简单格式
                        'format': '%(asctime)s %(levelname)s %(message)s',
                        # 输出时间、级别、消息
                        'datefmt': '%Y-%m-%d %H:%M:%S'
                    },
                    # ColoredFormatter的彩色输出（控制台用）
                    'colored': {
                        '()': 'colorlog.ColoredFormatter',
                        'format': "%(log_color)s%(asctime)s %(levelname)s:%(reset)s %(message_log_color)s%(message)s",
                        'datefmt': '%H:%M:%S',
                        'reset' : True,  # 开启重置颜色
                        'log_colors': {
                            'DEBUG': 'cyan',  # 青色
                            'INFO': 'green',  # 绿色
                            'WARNING': 'yellow',  # 黄色
                            'ERROR': 'bold_light_red',  # 红色(粗体)
                            'CRITICAL': 'bold_light_red',  # 亮红(粗体)
                        },
                        'secondary_log_colors': {
                            'message': {
                                'DEBUG': 'cyan',  # 青色
                                'INFO': 'light_green',  # 浅绿色
                                'WARNING': 'light_yellow',  # 浅黄色
                                'ERROR': 'red',  # 红色
                                'CRITICAL': 'red'  # 红色
                            }
                        },
                        'style': '%',
                    },
                },

                # 定义日志处理器
                'handlers': {
                    'console': {  # 控制台输出 handler
                        'class': 'colorlog.StreamHandler',  # 使用标准输出流
                        'level': 'INFO',  # 日志级别
                        'formatter': 'colored',  # 使用 colored 格式（需要有color库）
                        'stream': 'ext://sys.stdout'  # 输出到 stdout
                    },

                    'file': {  # 普通日志文件 handler（按天切分）
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'level': 'DEBUG',  # 写入的日志级别
                        'formatter': 'simple',  # 使用 simple 格式
                        'filename': f'{get_root()}/outputs/logs/日志记录.log',  # 日志文件路径
                        # 'filename': f'{get_root()}/日志记录.log',  # 日志文件路径
                        'when': 'midnight',  # 每天午夜切割日志
                        'interval': 1,  # 每 1 天切割一次
                        'backupCount': 2,  # 保留最近 2 个历史日志
                        'encoding': 'utf-8',  # 文件编码
                        'delay': True  # 延迟创建日志文件，首次写入时才创建
                    },

                    'error_file': {  # 仅记录错误级别以上的日志
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'level': 'ERROR',  # 只写入 ERROR 及以上日志
                        'formatter': 'verbose',  # 使用详细格式
                        'filename': f'{get_root()}/outputs/logs/error.log',  # 错误日志文件路径
                        # 'filename': f'{get_root()}/error.log',  # 错误日志文件路径
                        'when': 'midnight',  # 每天午夜切割
                        'interval': 1,
                        'backupCount': 2,  # 保留最近 7 天的日志
                        'encoding': 'utf-8',
                        'delay': True
                    }
                },

                'root': {  # 根 logger 配置
                    'level': 'DEBUG',  # 根 logger 日志级别
                    'handlers': ['console', 'file', 'error_file']  # 根 logger 绑定的 handler
                }
            }
            # 创建日志记录器(全局处理后跟着文件和控制台输出的处理器)
            logging.config.dictConfig(self.default_config)
            # 拿到日志记录器
            self.logger = logging.getLogger(LOGGER_NAME)
            # 启动全局异常捕获
            self.setup_exception_hook()

    # def ensure_path_exist(self):
    #     """确保日志输出目录确实存在
    #     默认是当有日志输出的时候才创建日志文件，所有这个的路径
    #     :return:有效的日志输出目录
    #     """
    #     if not is_logs_path_exist("./"):
    #         return create_logs_path()
    #     return get_root() / "outputs" / "logs"


    # def init_logger(self):
    #     """初始化日志记录器
    #
    #     :return:
    #     """
    #     # 创建日志记录器(全局处理后跟着文件和控制台输出的处理器)
    #     logging.config.dictConfig(self.default_config)
    #     # 拿到日志记录器
    #     self.logger = logging.getLogger("WebAIPilot.py")
    #     # 启动全局异常捕获
    #     self.setup_exception_hook()

    """自定义的日志配置"""
    def use_logging_config(self, config_manager: ConfigManager) -> bool:
        """使用自定义的日志配置更新当前日志管理器
        
        该方法会检查配置管理器中的日志配置是否包含错误信息，如果有则记录错误日志；
        如果没有错误，则使用新的配置重新配置日志记录器。

        :param config_manager: 配置管理器实例，包含日志配置信息
        :type config_manager: ConfigManager
        :return: True
        """
        # 判断日志配置器解析配置错误
        if config_manager.config is False:
            # # 确保日志输出目录和日志文件存在（打印和记录全局配置文件丢失的错误）
            # (create_logs_path() / "error.log").touch(exist_ok=True)
            # (create_logs_path() / "日志记录.log").touch(exist_ok=True)
            # 检查是否是日志解析的错误
            if hasattr(config_manager.logging_configurator, "error_msg"):
                # 存在错误信息属性，抛出错误
                msg, exc = config_manager.logging_configurator.error_msg
                error(msg, exc_info=exc)
            # 逆天bug，必须存在logs目录才输出错误信息，什么鬼？
            else:
                print(1)
        else:
            # 确保自定义日志配置的日志输出路径存在
            if not Path(config_manager.config_data["handlers"]["file"]["filename"]).parent.exists():
                mkdir(Path(config_manager.config_data["handlers"]["file"]["filename"]).parent)
            if not Path(config_manager.config_data["handlers"]["error_file"]["filename"]).parent.exists():
                mkdir(Path(config_manager.config_data["handlers"]["error_file"]["filename"]).parent)
            # 更新日志记录器(全局处理后跟着文件和控制台输出的处理器)
            logging.config.dictConfig(config_manager.config_data)
            # 更新日志记录器
            self.logger = logging.getLogger(LOGGER_NAME)
            # 安全删除默认配置(释放默认配置的空间)
            if hasattr(self, "default_config"):
                delattr(self, "default_config")
        return True

    def update_logging_config(self, config_data: dict) -> bool:
        """使用自定义的日志配置更新当前日志管理器
        使用新的配置重新配置日志记录器。
        :param config_data: 配置管理器实例，包含日志配置信息
        :type config_data: dict
        :return: config_data
        """
        # 更新日志记录器(全局处理后跟着文件和控制台输出的处理器)
        logging.config.dictConfig(config_data)
        # 更新日志记录器
        self.logger = logging.getLogger(LOGGER_NAME)
        # 安全删除默认配置(释放默认配置的空间)
        if hasattr(self, "default_config"):
            delattr(self, "default_config")
        return True


    def setup_exception_hook(self):
        """设置全局异常钩子"""
        def exception_hook(exc_type, exc_value, exc_traceback):
            """捕获未处理的异常
            参数： exc_type ： 捕获的异常类型
            exc_value ： 异常的值
            exc_traceback ： 异常返回的值
            """
            # 忽略键盘中断的异常，比如pycharm的停止运行或控制台的Ctrl+C
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return "忽略键盘中断的异常"

            return self.logger.exception("发生致命异常导致程序崩溃:", exc_info=(exc_type, exc_value, exc_traceback))

        # 启动函数：开启全局异常捕获
        sys.excepthook = exception_hook

# 创建单例实例
logger_manager = LoggerManager()

"""便捷函数（使用lambda减少代码量）"""
# 变量等级数据输出
debug = lambda msg, *args, **kwargs: logger_manager.logger.debug(msg, *args, **kwargs)
# 正常业务流程输出
info = lambda msg, *args, **kwargs: logger_manager.logger.info(msg, *args, **kwargs)
# 警告输出
warning = lambda msg, *args, **kwargs: logger_manager.logger.warning(msg, *args, **kwargs)
# 错误输出[非程序问题导致](场景： 业务逻辑判断出现错误，但没有抛出异常)检查用户输入的密码发现密码错误
error = lambda msg, *args, **kwargs: logger_manager.logger.error(msg, *args, **kwargs)
# 严重错误输出(整个程序崩溃)
critical = lambda msg, *args, **kwargs: logger_manager.logger.critical(msg, *args, **kwargs)

# exception需要特殊处理（默认包含堆栈信息）
def exception(
    msg: object,
    *args: object,
    exc_info: None | bool | BaseException | Tuple[Type[BaseException],
        BaseException, Optional[TracebackType]] = True,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Optional[Mapping[str, object]] = None
):
    """异常日志输出（自动附带堆栈信息）
    参数： msg ： 日志消息
    args ： 可变参数
    exc_info ： 异常信息参数
    stack_info ： 是否包含堆栈信息
    stacklevel ： 堆栈级别
    extra ： 额外信息
    """
    logger_manager.logger.exception(
        msg, *args,
        exc_info=exc_info,
        stack_info=stack_info,
        stacklevel=stacklevel,
        extra=extra
    )

# 测试代码
if __name__ == '__main__':
    debug("调试日志输出")
    info("运行正常日志输出")
    warning("警告日志输出")
    error("错误日志输出")
    critical("致命错误日志输出")
    try:
        raise Exception("测试异常")
    except Exception as e:
        # 不属于日志等级，仅仅是error的进阶版(栈区)
        exception("错误异常捕获日志输出:")
    # 除0错误，全局捕获(程序崩溃)
    a = 1 / 0
    pass