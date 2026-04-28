# 导入MongoDB连接模块
import mongodb_connect

# 获取MongoDB连接实例
mongodbClient = mongodb_connect.MongoDBConnect.getConnect()
# 连接到名为"python_database"的数据库
pythonDatabase = mongodbClient.get_database("python_database")
# 创建名为"baseCollection"的普通集合
pythonDatabase.create_collection("baseCollection")

# 创建一个固定大小的集合(capped collection)
# capped=True表示创建固定集合
# size=5242880表示集合大小为5MB(5*1024*1024字节)
# max=5000表示集合最多存储5000个文档
pythonDatabase.create_collection(
   "cappedCollection",
   capped=True,
   size=5242880,
   max=5000
)

# 定义时间序列集合的配置
# timeField:时间字段名
# metaField:元数据字段名
# granularity:时间粒度(此处为小时)
timeCollection = {
    "timeField":"timestamp",
    "metaField":"data",
    "granularity":"hours"
}

# 创建时间序列集合
# timeseries=timeCollection指定时间序列配置
# expireAfterSeconds=86400设置数据24小时后过期(86400秒)
pythonDatabase.create_collection(
    "weather24h",
    timeseries=timeCollection,
    expireAfterSeconds=86400
)

# 定义集群索引配置
# key:索引字段
# unique:是否唯一索引
# name:索引名称
clusteredCollection = {
    "key":{"_id":1},
    "unique":True,
    "name":"clusteredKey"
}

# 创建带有集群索引的集合
pythonDatabase.create_collection(
    "clusteredCollection",
    clusteredIndex=clusteredCollection
)

# 创建基于baseCollection的视图
# viewOn:指定基础集合
# pipeline:聚合管道，过滤year字段等于1的文档
pythonDatabase.create_collection(
    "myView",
    viewOn="baseCollection",
    pipeline=[{"$match": { "year": 1 }}]
)

# 列出数据库中的所有集合名称
collections = pythonDatabase.list_collection_names()

# 打印所有集合名称
for collection in collections:
    print(collection)

# 获取baseCollection集合的引用
baseCollection = pythonDatabase.get_collection("baseCollection")

# 删除集合clusteredCollection
pythonDatabase.drop_collection("clusteredCollection")
mongodbClient.close()