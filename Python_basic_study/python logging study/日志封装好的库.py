"""专门用于做日志记录处理
也方便直接调用
"""
# 系统库
import logging                  # logs
import sys                      # 系统库
from types import TracebackType # 重写方法需要
from typing import Mapping      # 重写方法需要

# 第三方库
import colorlog  # 颜色处理

# 记录器
log = logging.getLogger(__name__)  # 创建记录器
log.setLevel(logging.DEBUG)  # 设置为最低级别记录所有调试信息

# 创建流式处理器（控制台输出）
console_handler = colorlog.StreamHandler()  # 使用colorlog库创建彩色控制台处理器
# console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 设置日志等级

# 创建文件处理器（日志文件写入）
try:                        # 开发路径
    arisu_handler = logging.FileHandler(filename="logs/运行日志.log", encoding="utf8", mode="w")
except FileNotFoundError:   # 可能的测试路径
    try:
        arisu_handler = logging.FileHandler(filename="./logs/运行日志日志.log", encoding="utf8", mode="w")
    except FileNotFoundError:  # 当前目录
        arisu_handler = logging.FileHandler(filename="运行日志日志.log", encoding="utf8", mode="w")
arisu_handler.setLevel(logging.DEBUG)  # 设置日志等级为调试等级

# # 创建控制台输出格式
# consoleFormatter = logging.Formatter(
#     fmt="%(asctime)s %(levelname)s:%(message)s",  # 时间，等级，消息
#     datefmt="%H:%M:%S"                  # 时分秒
# )
# 创建彩色日志格式
console_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)s:%(reset)s %(message_log_color)s%(message)s",
    datefmt="%H:%M:%S",  # 时间格式为时分秒
    reset=True,  # 开启重置颜色
    log_colors={
        'DEBUG': 'cyan',  # 灰色
        'INFO': 'green',  # 绿色
        'WARNING': 'yellow',  # 黄色
        'ERROR': 'bold_light_red',  # 红色(粗体)
        'CRITICAL': 'bold_light_red',  # 量红(粗体)
    },
    secondary_log_colors={
        'message': {
            'DEBUG': 'cyan',
            'INFO': 'light_green',
            'WARNING': 'light_yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
    },
    style='%'
)
# 设置控制台处理器的文本的输出格式
console_handler.setFormatter(console_formatter)

# 创建文本文件的输出格式
fileFormatter = logging.Formatter(
    fmt="%(asctime)s:%(msecs)d %(levelname)s:%(message)s",  # 时间，等级，消息
    datefmt="%Y-%m-%d %H:%M:%S"  # 年月日，时分秒
)
# 设置文件处理的写入文本的输出格式（时间，等级名，消息）
arisu_handler.setFormatter(fileFormatter)

# 记录器添加处理器
log.addHandler(console_handler)  # 控制台
log.addHandler(arisu_handler)  # 文件


def exception_hook(type, value, traceback):
    """捕获未处理的异常
    参数： type ： 捕获的异常类型
    value ： 异常的值
    traceback ： 异常返回的值
    """
    # 忽略键盘中断的异常，比如pycharm的停止运行或控制台的Ctrl+C
    if issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, traceback)
        return
    # 记录未捕获的异常
    log.critical("发生致命异常导致程序崩溃:", exc_info=(type, value, traceback))

sys.excepthook = exception_hook # 开启全局异常捕获

log.info("主程序开始(导包完成，全局异常捕获加载完成)")

"""=======================================================方法定义=================================================================="""
# def debug(msg: object,
#           *args: object,
#           exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[
#               None, None, None] | BaseException = None,
#           stack_info: bool = False,
#           stacklevel: int = 1,
#           extra: Mapping[str, object] | None = None) -> None:
#     """调试日志输出"""
#     # log.debug(f"\033[90m{message}\033[0m")
#     log.debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def debug(msg: object,*args: object):
    """调试日志输出"""
    # log.debug(f"\033[90m{message}\033[0m")
    log.debug(msg, *args)

# def info(msg: object,
#          *args: object,
#          exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[
#              None, None, None] | BaseException = None,
#          stack_info: bool = False,
#          stacklevel: int = 1,
#          extra: Mapping[str, object] | None = None) -> None:
#     """运行正常日志输出"""
#     # log.info(f"\033[97m{message}\033[0m")
#     log.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
def info(msg: object,*args: object):
    """运行正常日志输出"""
    log.info(msg, *args)

# def warning(msg: object,
#             *args: object,
#             exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[
#                 None, None, None] | BaseException = None,
#             stack_info: bool = False,
#             stacklevel: int = 1,
#             extra: Mapping[str, object] | None = None) -> None:
#     """警告日志输出"""
#     # log.warning(f"\033[93m{message}\033[0m")
#     log.warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def warning(msg: object,*args: object):
    """警告日志输出"""
    log.warning(msg, *args)

# def critical(msg: object,
#              *args: object,
#              exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[
#                  None, None, None] | BaseException = None,
#              stack_info: bool = False,
#              stacklevel: int = 1,
#              extra: Mapping[str, object] | None = None) -> None:
#     """致命错误日志输出"""
#     # log.critical(f"\033[31m{message}\033[0m")
#     log.critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def critical(msg: object,*args: object):
    """致命错误日志输出"""
    log.critical(msg, *args)

# def exception(msg: object,
#              *args: object,
#              exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None,
#              stack_info: bool = False,
#              stacklevel: int = 1,
#              extra: Mapping[str, object] | None = None) -> None:
#     """异常捕获日志输出（比致命错误日志输出强）"""
#     # 保持原始调用，颜色应由日志处理器控制
#     log.exception(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def exception(msg: object,*args: object):
    """异常捕获日志输出（比致命错误日志输出强）"""
    # 保持原始调用，颜色应由日志处理器控制
    log.exception(msg, *args)


if __name__ == '__main__':
    debug("调试日志输出")
    info("运行正常日志输出")
    warning("警告日志输出")
    # critical("致命错误日志输出")
    exception("异常捕获日志输出")
    a = 1 / 0