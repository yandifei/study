# 记录日志到文件
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

"""
如果你想从命令行设置日志级别，例如：

--log=INFO
并且你将 --log 命令的参数存进了变量 loglevel，你可以用：

Copy
getattr(logging, loglevel.upper())
"""

"""
记录变量数据
要记录变量数据，请使用格式字符串作为事件描述消息，并附加传入变量数据作为参数。 例如:

import logging
logging.warning('%s before you %s', 'Look', 'leap!')
将显示：

WARNING:root:Look before you leap!
"""
