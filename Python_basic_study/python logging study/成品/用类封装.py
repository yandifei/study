"""专门用于做日志记录处理，方便直接调用"""
# 系统库
import sys  # 系统库
import threading  # 线程库，用于线程锁
import logging  # 日志记录库
# import logging.config   # 解析日志配置
# from logging.handlers import RotatingFileHandler  # 日志大小轮转处理器
from logging.handlers import TimedRotatingFileHandler  # 日志时间轮转处理器
from sys import exc_info
from types import TracebackType
from typing import Mapping, Optional, Type, Union, Tuple
# 第三方库
import colorlog  # 颜色处理库

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
        """初始化日志管理器"""
        # 确保配置只加载一次(Pythonic写法)
        if not hasattr(self, '_initialized'):
            # 创建一个日志记录器(全局处理后跟着文件和控制台输出的处理器)
            self.logger = self.get_logger() # 必须确保只调用了一次
            # 启动全局异常捕获
            self.setup_exception_hook()
            # 设置实例化标志位
            self._initialized = True

    def get_logger(self) -> logging.Logger:
        """获取或创建一个logger（延迟初始化）
        全局日志记录器后创建子处理器去管理（确保只调用了一次，不然会有多个输出）
        :return: 配置好的logger实例
        """
        # 记录器(全局的)
        logger = logging.getLogger("WebAIPilot.py")
        # 设置为最低级别记录所有调试信息（这个就不要动了，这个是全局的处理器）
        logger.setLevel(logging.DEBUG)
        # 不向上层 root logger 传播，避免重复输出
        logger.propagate = False

        # 添加处理器（控制台会输出颜色，所以必须放最后，不然日志会加入ASCII字符）
        # 文件处理器
        logger.addHandler(self.create_file_handler())
        # 错误文件处理器
        logger.addHandler(self.create_err_file_handler())
        # 控制台处理器
        logger.addHandler(self.create_console_handler())

        return logger

    @staticmethod
    def create_console_handler():
        """创建控制台处理器
        :return: 配置好的控制台处理器
        """
        # 创建流式处理器（控制台输出）
        handler = colorlog.StreamHandler(stream=sys.stderr)
        # 控制台只显示 INFO 及以上日志
        handler.setLevel(logging.INFO)

        # 创建彩色日志格式（统一输出格式：21:08:25 INFO:消息内容）
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)s:%(reset)s %(message_log_color)s%(message)s",
            datefmt="%H:%M:%S",  # 时间格式为时分秒
            reset=True,  # 开启重置颜色
            log_colors={
                'DEBUG': 'cyan',  # 青色
                'INFO': 'green',  # 绿色
                'WARNING': 'yellow',  # 黄色
                'ERROR': 'bold_light_red',  # 红色(粗体)
                'CRITICAL': 'bold_light_red',  # 亮红(粗体)
            },
            secondary_log_colors={
                'message': {
                    'DEBUG': 'cyan',  # 青色
                    'INFO': 'light_green',  # 浅绿色
                    'WARNING': 'light_yellow',  # 浅黄色
                    'ERROR': 'red',  # 红色
                    'CRITICAL': 'red'  # 红色
                }
            },
            style='%'
        )
        # 设置控制台处理器的文本的输出格式
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_file_handler():
        """创建文件处理器
        使用的是时间轮转处理器,每个文件1MB，保留3个备份
        :return: 配置好的文件处理器
        """
        # 创建文件处理器（日志文件写入）时间轮转
        handler = TimedRotatingFileHandler(
            # filename="../outputs/logs/日志记录.log",  # 日志文件路径
            filename="outputs/logs/日志记录.log",  # 日志文件路径
            when="midnight",  # 每天 0 点轮转
            interval=1,  # 每 1 天轮转一次
            backupCount=30,  # 保留 30 天历史日志
            encoding="utf-8",  # 文件编码
            delay=True  # 延迟文件创建
        )
        # 设置日志等级为调试等级
        handler.setLevel(logging.DEBUG)

        # 创建文本文件的输出格式
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",  # 时间，等级，消息
            datefmt="%Y-%m-%d %H:%M:%S"  # 年月日，时分秒
        )
        # 设置文件处理的写入文本的输出格式（时间，等级名，消息）
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_err_file_handler():
        """创建错误文件处理器
        :return: 配置好的文件处理器
        """
        # 创建错误文件处理器（日志文件写入）时间轮转
        handler = TimedRotatingFileHandler(
            # filename="../outputs/logs/error.log",  # 日志文件路径
            filename="outputs/logs/error.log",  # 日志文件路径
            when="midnight",  # 每天 0 点轮转
            interval=1,  # 每 1 天轮转一次
            backupCount=30,  # 保留 30 天历史日志
            encoding="utf-8",  # 文件编码
            delay=True  # 延迟文件创建
        )
        # 设置日志等级为调试等级
        handler.setLevel(logging.ERROR)

        # 创建文本文件的输出格式
        formatter = logging.Formatter(
            # fmt="%(asctime)s:%(msecs)d %(levelname)s:%(message)s",  # 时间，等级，消息
            # 含时间、级别、模块、行号、线程、日志信息
            fmt="%(asctime)s %(levelname)s %(name)s:%(lineno)d %(threadName)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"  # 年月日，时分秒
        )
        # 设置文件处理的写入文本的输出格式（时间，等级名，消息）
        handler.setFormatter(formatter)
        return handler

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
                return

            self.logger.exception("发生致命异常导致程序崩溃:", exc_info=(exc_type, exc_value, exc_traceback))

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