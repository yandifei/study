from pymongo import MongoClient
class MongoDBConnect:
    default_uri = ("mongodb://itcastAdmin:123456@"
                   "192.168.121.134:27016/?authSource=admin")
    @staticmethod
    def getConnect(uri=default_uri):
        client = MongoClient(uri)
        return client
