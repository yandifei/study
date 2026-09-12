"""
MongoDB Python驱动程序完整操作示例
包含数据库、集合、文档的完整CRUD操作
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime
import pprint


class MongoDBOperations:
    """MongoDB操作类，封装所有数据库操作"""

    def __init__(self):
        self.uri = "mongodb://localhost:27017/"
        self.client = None
        self.db = None

    def connect(self):
        """建立与MongoDB的连接"""
        try:
            # uri: MongoDB连接字符串，指定连接的数据库服务器地址
            # serverSelectionTimeoutMS: 服务器选择超时时间，单位为毫秒，这里设置为5000ms(5秒)
            # directConnection: 是否直接连接到服务器，设置为True表示直接连接，不使用副本集自动发现
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000, directConnection=True)
            # 测试连接
            self.client.admin.command('ping')
            print("✓ 成功连接到MongoDB服务器")
            print(f"  MongoDB版本: {self.client.server_info()['version']}")
            return True
        except ConnectionFailure as e:
            print(f"✗ 连接失败: {e}")
            return False
        except Exception as e:
            print(f"✗ 其他错误: {e}")
            return False

    def disconnect(self):
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()
            print("✓ 已关闭MongoDB连接")

    # -------------------- 数据库操作 --------------------
    def list_databases(self):
        """查看所有数据库"""
        print("\n" + "=" * 50)
        print("【数据库操作】查看所有数据库")
        print("=" * 50)
        databases = self.client.list_database_names()
        for i, db_name in enumerate(databases, 1):
            try:
                db_stats = self.client[db_name].command("dbStats")
                size_mb = db_stats['dataSize'] / 1024 / 1024
                print(f"{i}. {db_name} - 大小: {size_mb:.2f} MB")
            except:
                print(f"{i}. {db_name}")
        return databases

    def access_database(self, db_name):
        """访问指定数据库"""
        print("\n" + "=" * 50)
        print(f"【数据库操作】访问数据库: {db_name}")
        print("=" * 50)
        self.db = self.client[db_name]
        print(f"✓ 成功访问数据库: {db_name}")
        print(f"  数据库中的集合数量: {len(self.db.list_collection_names())}")
        return self.db

    def create_database(self, db_name):
        """创建数据库（MongoDB中数据库会在第一次插入数据时自动创建）"""
        print("\n" + "=" * 50)
        print(f"【数据库操作】创建数据库: {db_name}")
        print("=" * 50)
        temp_db = self.client[db_name]
        temp_collection = temp_db['_temp_collection']
        result = temp_collection.insert_one({
            "message": "临时文档，用于创建数据库",
            "created_at": datetime.now()
        })
        temp_collection.drop()
        print(f"✓ 成功创建数据库: {db_name}")
        return temp_db

    def delete_database(self, db_name):
        """删除指定数据库"""
        print("\n" + "=" * 50)
        print(f"【数据库操作】删除数据库: {db_name}")
        print("=" * 50)
        try:
            if db_name in self.client.list_database_names():
                self.client.drop_database(db_name)
                print(f"✓ 成功删除数据库: {db_name}")
            else:
                print(f"⚠ 数据库 {db_name} 不存在")
        except OperationFailure as e:
            print(f"✗ 删除失败: {e}")

    # -------------------- 集合操作 --------------------
    def create_collection(self, collection_name, capped=False, size=None):
        """创建集合"""
        print("\n" + "=" * 50)
        print(f"【集合操作】创建集合: {collection_name}")
        print("=" * 50)
        if self.db is None:
            print("✗ 请先访问或创建数据库")
            return None
        try:
            # 如果集合已存在，先删除
            if collection_name in self.db.list_collection_names():
                self.db[collection_name].drop()
                print(f"⚠ 集合 {collection_name} 已存在，已删除旧集合")
            
            options = {}
            if capped:
                options['capped'] = True
                options['size'] = size or 1048576
            collection = self.db.create_collection(collection_name, **options)
            print(f"✓ 成功创建集合: {collection_name}")
            if capped:
                print(f"  集合类型: 固定集合 (大小: {options['size']} bytes)")
            return collection
        except OperationFailure as e:
            print(f"✗ 创建集合失败: {e}")
            return None

    def create_view(self, view_name, source_collection, pipeline):
        """创建视图"""
        print("\n" + "=" * 50)
        print(f"【集合操作】创建视图: {view_name}")
        print("=" * 50)
        if self.db is None:
            print("✗ 请先访问或创建数据库")
            return None
        try:
            # 如果视图已存在，先删除
            if view_name in self.db.list_collection_names():
                self.db[view_name].drop()
                print(f"⚠ 视图 {view_name} 已存在，已删除旧视图")
            
            if source_collection not in self.db.list_collection_names():
                self.db[source_collection].insert_many([
                    {"name": "张三", "age": 25, "city": "北京"},
                    {"name": "李四", "age": 30, "city": "上海"},
                    {"name": "王五", "age": 28, "city": "广州"}
                ])
            self.db.create_collection(view_name, viewOn=source_collection, pipeline=pipeline)
            print(f"✓ 成功创建视图: {view_name}")
            print(f"  基于集合: {source_collection}")
            print(f"  聚合管道: {pipeline}")
            return self.db[view_name]
        except OperationFailure as e:
            print(f"✗ 创建视图失败: {e}")
            return None

    def list_collections(self):
        """查看当前数据库中的所有集合"""
        print("\n" + "=" * 50)
        print("【集合操作】查看所有集合")
        print("=" * 50)
        if self.db is None:
            print("✗ 请先访问或创建数据库")
            return []
        collections = self.db.list_collection_names()
        if not collections:
            print("当前数据库中没有任何集合")
        else:
            for i, coll_name in enumerate(collections, 1):
                print(f"{i}. {coll_name}")
        return collections

    def access_collection(self, collection_name):
        """访问指定集合"""
        print("\n" + "=" * 34)
        print(f"【集合操作】访问集合: {collection_name}")
        print("=" * 34)
        if self.db is None:
            print("✗ 请先访问或创建数据库")
            return None
        collection = self.db[collection_name]
        print(f"✓ 成功访问集合: {collection_name}")
        return collection

    def delete_collection(self, collection_name):
        """删除指定集合"""
        print("\n" + "=" * 50)
        print(f"【集合操作】删除集合: {collection_name}")
        print("=" * 50)
        if self.db is None:
            print("✗ 请先访问或创建数据库")
            return
        try:
            if collection_name in self.db.list_collection_names():
                self.db[collection_name].drop()
                print(f"✓ 成功删除集合: {collection_name}")
            else:
                print(f"⚠ 集合 {collection_name} 不存在")
        except OperationFailure as e:
            print(f"✗ 删除失败: {e}")

    # -------------------- 文档操作 --------------------
    def insert_documents(self, collection_name, documents):
        """插入文档（自动判断单条或多条）"""
        print("\n" + "=" * 50)
        print(f"【文档操作】插入文档到集合: {collection_name}")
        print("=" * 50)
        collection = self.access_collection(collection_name)
        if collection is None:
            return None
        try:
            if isinstance(documents, dict):
                result = collection.insert_one(documents)
                print(f"✓ 成功插入1条文档")
                print(f"  插入的文档ID: {result.inserted_id}")
                return result.inserted_id
            else:
                result = collection.insert_many(documents)
                print(f"✓ 成功插入{len(documents)}条文档")
                print(f"  插入的文档ID: {result.inserted_ids}")
                return result.inserted_ids
        except OperationFailure as e:
            print(f"✗ 插入文档失败: {e}")
            return None

    def query_documents(self, collection_name, filter=None, projection=None, limit=0):
        """查询文档"""
        print("\n" + "=" * 50)
        print(f"【文档操作】查询集合中的文档: {collection_name}")
        print("=" * 50)
        collection = self.access_collection(collection_name)
        if collection is None:
            return []
        try:
            if filter is None:
                filter = {}
            cursor = collection.find(filter, projection)
            if limit > 0:
                cursor = cursor.limit(limit)
            total_count = collection.count_documents(filter)
            print(f"查询条件: {filter}")
            print(f"返回字段: {projection if projection else '所有字段'}")
            print(f"符合条件的文档总数: {total_count}")
            results = list(cursor)
            if results:
                print(f"\n查询结果 (显示前{min(5, len(results))}条):")
                for i, doc in enumerate(results[:5], 1):
                    print(f"\n文档 {i}:")
                    pprint.pprint(doc)
            else:
                print("没有找到符合条件的文档")
            return results
        except OperationFailure as e:
            print(f"✗ 查询文档失败: {e}")
            return []

    def update_documents(self, collection_name, filter, update, update_many=False):
        """更新文档"""
        print("\n" + "=" * 50)
        print(f"【文档操作】更新集合中的文档: {collection_name}")
        print("=" * 50)
        collection = self.access_collection(collection_name)
        if collection is None:
            return None
        try:
            print(f"更新条件: {filter}")
            print(f"更新操作: {update}")
            if update_many:
                result = collection.update_many(filter, update)
                print(f"✓ 成功更新 {result.modified_count} 条文档")
                print(f"  匹配文档数: {result.matched_count}")
            else:
                result = collection.update_one(filter, update)
                print(f"✓ 成功更新 {result.modified_count} 条文档")
                print(f"  匹配文档数: {result.matched_count}")
            return result
        except OperationFailure as e:
            print(f"✗ 更新文档失败: {e}")
            return None

    def delete_documents(self, collection_name, filter, delete_many=False):
        """删除文档"""
        print("\n" + "=" * 50)
        print(f"【文档操作】删除集合中的文档: {collection_name}")
        print("=" * 50)
        collection = self.access_collection(collection_name)
        if collection is None:
            return None
        try:
            print(f"删除条件: {filter}")
            if delete_many:
                result = collection.delete_many(filter)
                print(f"✓ 成功删除 {result.deleted_count} 条文档")
            else:
                result = collection.delete_one(filter)
                print(f"✓ 成功删除 {result.deleted_count} 条文档")
            return result
        except OperationFailure as e:
            print(f"✗ 删除文档失败: {e}")
            return None


if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Python驱动程序完整操作演示")
    print("=" * 60)

    mongo_ops = MongoDBOperations()
    if not mongo_ops.connect():
        print("程序终止")
        exit()

    # ---------- 数据库操作演示 ----------
    print("\n" + "█" * 60)
    print("█ 第一部分：数据库操作")
    print("█" * 60)
    mongo_ops.list_databases()
    test_db_name = "python_test_db"
    mongo_ops.create_database(test_db_name)
    mongo_ops.access_database(test_db_name)

    # ---------- 集合操作演示 ----------
    print("\n" + "█" * 60)
    print("█ 第二部分：集合操作")
    print("█" * 60)
    mongo_ops.create_collection("users")
    mongo_ops.create_collection("logs", capped=True, size=1048576)
    view_pipeline = [{"$match": {"age": {"$gte": 25}}}]
    mongo_ops.create_view("adult_users_view", "users", view_pipeline)
    mongo_ops.list_collections()

    # ---------- 文档操作演示 ----------
    print("\n" + "█" * 60)
    print("█ 第三部分：文档操作")
    print("█" * 60)
    single_doc = {
        "name": "张三", "age": 25, "email": "zhangsan@example.com",
        "city": "北京", "created_at": datetime.now()
    }
    multiple_docs = [
        {"name": "李四", "age": 30, "email": "lisi@example.com", "city": "上海", "score": 85},
        {"name": "王五", "age": 28, "email": "wangwu@example.com", "city": "广州", "score": 92},
        {"name": "赵六", "age": 22, "email": "zhaoliu@example.com", "city": "深圳", "score": 78},
        {"name": "孙七", "age": 35, "email": "sunqi@example.com", "city": "北京", "score": 88},
        {"name": "周八", "age": 26, "email": "zhouba@example.com", "city": "上海", "score": 95}
    ]
    mongo_ops.insert_documents("users", single_doc)
    mongo_ops.insert_documents("users", multiple_docs)

    # 查询
    mongo_ops.query_documents("users", {}, limit=10)
    mongo_ops.query_documents("users", {"city": "北京"})
    mongo_ops.query_documents("users", {"age": {"$gte": 28}})
    mongo_ops.query_documents("users", {"city": "上海"}, {"name": 1, "age": 1, "_id": 0})

    # 更新
    mongo_ops.update_documents("users", {"name": "张三"}, {"$set": {"age": 26, "city": "上海"}})
    mongo_ops.update_documents("users", {"city": "北京"}, {"$inc": {"age": 1}}, update_many=True)
    print("\n验证更新结果:")
    mongo_ops.query_documents("users", {"city": "北京"})

    # 删除
    mongo_ops.delete_documents("users", {"name": "赵六"})
    mongo_ops.delete_documents("users", {"score": {"$lt": 80}}, delete_many=True)
    print("\n验证删除结果:")
    mongo_ops.query_documents("users", {}, limit=10)

    # ---------- 清理测试数据 ----------
    print("\n" + "█" * 60)
    print("█ 第四部分：清理测试数据")
    print("█" * 60)
    mongo_ops.delete_collection("users")
    mongo_ops.delete_collection("logs")
    mongo_ops.delete_collection("adult_users_view")
    mongo_ops.delete_database("python_test_db")


    mongo_ops.disconnect()
    print("\n" + "=" * 60)
    print("所有操作演示完成！")
    print("=" * 60)