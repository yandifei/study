# 导包
from pyspark import SparkConf, SparkContext
# 创建类对象
conf = SparkConf().setMaster("local[*]").setAppName("test_spark_app")
# 基于SparkConf类对象创建SparkContext对象
sc = SparkContext(conf=conf)
# 打印PySpark的运行版本
print(sc.version)
# 停止SparkContext对象的运行(停止PySpark程序)
sc.stop()



"""
这个学个鸡毛，学不了一点（环境都不对，真的是fuck ）
"""