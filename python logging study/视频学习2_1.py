# 使用配置文件来管理日志
import logging
import logging.config


# 配置文件的方式来处理(python3.2之后推荐的配置方式为字典)
# 记录器

# logging.config.fileConfig("logging.conf",encoding="utf8")   # 其实这个是ini格式
logging.config.dictConfig({"loggers" : "root, applog"})   # 其实这个是json格式


rootLogger = logging.getLogger()
rootLogger.debug("这是一个root日志，debug")

logger = logging.getLogger("applog")
logger.debug("这是一个applog,debug")

# 1.编程式使用日志
# 2.logging格式的配置文件
# 3.字典方式的配置文件