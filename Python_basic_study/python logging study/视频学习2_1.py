# ʹ�������ļ���������־
import logging
import logging.config


# �����ļ��ķ�ʽ������(python3.2֮���Ƽ������÷�ʽΪ�ֵ�)
# ��¼��

# logging.config.fileConfig("logging.conf",encoding="utf8")   # ��ʵ�����ini��ʽ
logging.config.dictConfig({"loggers" : "root, applog"})   # ��ʵ�����json��ʽ


rootLogger = logging.getLogger()
rootLogger.debug("����һ��root��־��debug")

logger = logging.getLogger("applog")
logger.debug("����һ��applog,debug")

# 1.���ʽʹ����־
# 2.logging��ʽ�������ļ�
# 3.�ֵ䷽ʽ�������ļ�