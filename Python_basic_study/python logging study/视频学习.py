import logging

# 全局的
logging.basicConfig(filename="log.txt", filemode="w",
                    format="%(asctime)s - %(name)s － %(levelname)s - %(message)s",
                    level=logging.INFO, encoding="utf-8"
                    )

logging.debug("1")
logging.info("2")
logging.warning("3")
logging.error("4")
logging.critical("5")

# 单独的
test_logger = logging.getLogger("test_log") # 非全局的记录器（自定义解释器名）
# logging.getLogger(__name__) # 如果是import则__name__为文件名本身，如果是这个文件运行的则是__main__
file_handler = logging.FileHandler("test_log.txt", mode="w", encoding="utf8")    # basicConfig大多数设置都在这
file_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
test_logger.addHandler(file_handler)
test_logger.error("我是独立的logging")



