"""专门用于做日志记录处理
也方便直接调用
"""
# 系统库
import logging  # logs
import sys  # 系统库
from logging.handlers import RotatingFileHandler  # 日志大小轮转处理器
from types import TracebackType
from typing import Mapping

# 第三方库
import colorlog  # 颜色处理

# 记录器(全局的)
logger = logging.getLogger("WebAIPilot.py")  # 创建记录器
# 设置为最低级别记录所有调试信息（这个就不要动了，这个是全局的处理器）
logger.setLevel(logging.DEBUG)
# 不向上层 root logger 传播，避免重复输出
logger.propagate = False


def create_handler():
    """
    创建处理器（输出处理器和文件处理器）
    :return:
    """
    """创建流式处理器（控制台输出）"""
    console_handler = colorlog.StreamHandler(stream=sys.stderr)  # 使用colorlog库创建彩色控制台处理器
    console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 及以上日志

    # 创建控制台输出格式
    # console_formatter = logging.Formatter(
    #     fmt="%(asctime)s %(levelname)s:%(message)s",  # 时间，等级，消息
    #     datefmt="%H:%M:%S"                  # 时分秒
    # )
    # 创建彩色日志格式（统一输出格式：2025-12-08 21:08:25 INFO:消息内容）
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

    """创建文件处理器（日志文件写入。使用的是时间轮转处理器,每个文件1MB，保留3个备份）"""
    file_handler = RotatingFileHandler(
        filename="../outputs/logs/日志记录.log",  # 日志文件路径
        encoding="utf8",  # 文件编码
        mode="a",  # 追加写入
        maxBytes=1 * 1024 * 1024,  # 单文件最大 1MB 时轮转
        backupCount=3,  # 最多保留 3 个历史文件
    )
    # 设置日志等级为调试等级
    file_handler.setLevel(logging.DEBUG)

    # 创建文本文件的输出格式
    file_formatter = logging.Formatter(
        fmt="%(asctime)s:%(msecs)d %(levelname)s:%(message)s",  # 时间，等级，消息
        datefmt="%Y-%m-%d %H:%M:%S"  # 年月日，时分秒
    )
    # 设置文件处理的写入文本的输出格式（时间，等级名，消息）
    file_handler.setFormatter(file_formatter)

    return console_handler, file_handler

# 记录器添加两个处理器
console_handler, file_handler = create_handler()     # 获取根记录器
logger.addHandler(console_handler)  # 添加控制台处理器
logger.addHandler(file_handler)  # 添加文件处理器
"""=======================================================全局异常捕获=================================================================="""
def exception_hook(exception_type, exception_value, exception_traceback):
    """捕获未处理的异常
    参数： exception_type ： 捕获的异常类型
    exception_value ： 异常的值
    exception_traceback ： 异常返回的值
    """
    # 忽略键盘中断的异常，比如pycharm的停止运行或控制台的Ctrl+C
    if issubclass(exception_type, KeyboardInterrupt):
        sys.__excepthook__(exception_type, exception_value, exception_traceback)
        return
    # error_msg = ''.join(traceback.format_exception(exception_type, exception_value, exception_traceback))
    # 记录未捕获的异常
    # critical(f"发生致命异常导致程序崩溃:")
    logger.exception("发生致命异常导致程序崩溃:", exc_info=(exception_type, exception_value, exception_traceback))


# 启动函数
sys.excepthook = exception_hook  # 开启全局异常捕获
logger.info("主程序开始(导包完成，全局异常捕获加载完成)")

"""===================================================便捷方法================================================="""
def debug(
    msg: object,
    *args: object,
    exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
):
    """调试级别日志输出"""
    logger.debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def info(
    msg: object,
    *args: object,
    exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
):
    """普通信息日志输出"""
    logger.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def warning(
    msg: object,
    *args: object,
    exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
):
    """警告级别日志输出"""
    logger.warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def critical(
    msg: object,
    *args: object,
    exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
):
    """致命错误日志输出"""
    logger.critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

def exception(
    msg: object,
    *args: object,
    exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None,
    stack_info: bool = True,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
):
    """
    异常日志输出（等同于 error(exc_info=True)，会自动附带堆栈信息）
    由于 logger.exception() 默认设置 exc_info=True，这里传入的 exc_info 参数会被忽略，但是我还是加上了
    """
    logger.exception(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

if __name__ == '__main__':
    debug("调试日志输出")
    info("运行正常日志输出")
    warning("警告日志输出")
    critical("致命错误日志输出")
    try:
        a = 1 / 0
    except Exception as e:
        exception("异常捕获日志输出:")
