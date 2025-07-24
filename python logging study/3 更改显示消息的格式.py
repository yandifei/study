import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')


"""
注意在前面例子中出现的 “root” 已消失。
文档 LogRecord 属性 列出了可在格式字符串中出现的所有内容，但在简单的使用场景中，
你只需要 levelname （严重性）、message （事件描述，包含可变的数据）或许再加上事件发生的时间。
 这将在下一节中介绍。
"""