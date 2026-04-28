from pymongo import MongoClient
class MongoDBConnect:

    default_uri = ("mongodb://yandifei:yandifei@"
                   "127.0.0.1:27017/?authSource=admin")
    @staticmethod
    def getConnect(uri=default_uri):
        # 创建MongoDB客户端连接
        # 使用MongoClient类建立与MongoDB服务器的连接
        # 参数说明:
        # uri: MongoDB连接字符串，指定连接的数据库服务器地址
        # serverSelectionTimeoutMS: 服务器选择超时时间，单位为毫秒，这里设置为5000ms(5秒)
        # directConnection: 是否直接连接到服务器，设置为True表示直接连接，不使用副本集自动发现
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, directConnection=True)
        return client

if __name__ == '__main__':
    mongodbClient = MongoDBConnect.getConnect()
    databaseNames = mongodbClient.list_database_names()