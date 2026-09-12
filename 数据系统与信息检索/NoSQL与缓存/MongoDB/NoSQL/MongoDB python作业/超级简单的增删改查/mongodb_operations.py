from pymongo import MongoClient

# 连接 MongoDB（默认 localhost:27017，无认证）
client = MongoClient('localhost', 27017)
db = client['test_db']          # 使用（或自动创建）数据库 test_db

# 1. 创建集合（如果已存在则先删除，保证干净演示）
if 'users' in db.list_collection_names():
    db['users'].drop()
db.create_collection('users')
print('1. 集合创建成功')

# 2. 查看集合
print('2. 当前所有集合：', db.list_collection_names())

# 3. 插入一个文档
db.users.insert_one({'name': '张三', 'age': 30})
print('3. 文档插入成功')

# 4. 查看集合中的所有文档
print('4. 集合中的文档：')
for doc in db.users.find():
    print(doc)

# 5. 删除指定文档（删除 name 为“张三”的文档）
db.users.delete_one({'name': '张三'})
print('5. 指定文档删除成功')

client.close()