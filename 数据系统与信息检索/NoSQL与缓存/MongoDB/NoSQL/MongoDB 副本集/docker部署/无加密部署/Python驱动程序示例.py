# yandifei
from pymongo import MongoClient

# 副本集连接（推荐）
client = MongoClient(
    "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0"
)
db = client.testdb

# 写操作会自动发送到PRIMARY
result = db.testCollection.insert_one({"msg": "Hello Replica Set"})

# 读操作可配置读偏好
from pymongo.read_preferences import ReadPreference
secondary_db = client.get_database(
    "testdb",
    read_preference=ReadPreference.SECONDARY_PREFERRED
)
#

# 自己写个输出显示，不然都不知道是否成功
print(f"插入成功，文档ID: {result.inserted_id}")
docs = list(secondary_db.testCollection.find())
print(f"查询到 {len(docs)} 条文档:")
for doc in docs:
    print(doc)