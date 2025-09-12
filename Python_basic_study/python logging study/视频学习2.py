import logging
import sys

# 编程的方式来写一下高级的写法
# 记录器
logger = logging.getLogger("cn.cccb.applog")    # 创建记录器
logger.setLevel(logging.INFO)  # 设置记录等级
print(logger)
print(type(logger))


# 处理器handler(1这是流式处理器)
consoleHandler = logging.StreamHandler(stream=sys.stdout)    # 流式处理器（控制台输出）
consoleHandler.setLevel(logging.DEBUG)

# 处理器handler(2这是文件处理器)(没有给handler指定日志级别，将使用logger的级别)
fileHandler = logging.FileHandler(filename="文件处理器学习.log",encoding="utf8",mode="w")


# 创建formatter格式(-8可以最对齐，默认右对齐)
formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | 文件名:%(filename)s 行号:%(lineno)s | %(message)s")
# 给处理器设置格式
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)


# 记录器要设置处理器(示例为一个logger记录器有2个处理器)
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)


# 打印日志的代码
logger.debug("1")
logger.info("2")
logger.warning("3")
logger.error("4")
logger.critical("5")


"""过滤器学习"""
# 创建一个过滤器
flt = logging.Filter("cn.cccb")

# 关联过滤器
logger.addFilter(flt)   # 给logger添加这个过滤器
# fileHandler.addFilter(flt)  # 给fileHandel加过滤器

# 打印日志的代码
logger.debug("使用过滤器：1")
logger.info("使用过滤器：2")
logger.warning("使用过滤器：3")
logger.error("使用过滤器：4")
logger.critical("使用过滤器：5")