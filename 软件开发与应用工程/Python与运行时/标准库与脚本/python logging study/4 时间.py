# 注意logging.basicConfig(format='%(asctime)s %(message)s')只能有一条，多了遵循最开始的那条

"""
在消息中显示日期/时间
要显示事件的日期和时间，你可以在格式字符串中放置 '%(asctime)s'
"""
# import logging"""
# logging.basicConfig(format='%(asctime)s %(message)s')
# logging.warning('is when this event was logged.')


"""
日期/时间显示的默认格式（如上所示）类似于 ISO8601 或 RFC 3339 。
 如果你需要更多地控制日期/时间的格式，请为 basicConfig 提供 datefmt 参数，如下例所示:
datefmt 参数的格式与 time.strftime() 支持的格式相同。

import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')


"""
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S')
logging.warning('is when this event was logged.')

