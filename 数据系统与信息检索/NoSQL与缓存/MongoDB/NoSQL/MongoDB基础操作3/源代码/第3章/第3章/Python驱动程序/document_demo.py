from datetime import datetime
import mongodb_connect
def insert_document(collection):
    collection.insert_one(
        {
            "username": "星空下的吉他",
            "email": "xkxdjt@example.com",
            "age": 30,
            "is_active": False,
            "registration_date": datetime.now(),
            "address": {
                "provice": "广东省",
                "city": "广州市",
                "district": "天河区"
            },
            "interests": ["音乐", "吉他"],
            "signature": "音乐是灵魂的语言"
        }
    )
    collection.insert_many(
        [
            {
                "_id": 1,
                "username": "追梦赤子心",
                "email": "zmczx@example.com",
                "age": 30,
                "is_active": True,
                "registration_date": datetime.now(),
                "address": {
                    "provice": "山东省",
                    "city": "青岛市",
                    "district": "崂山区"
                },
                "interests": ["读书", "旅行", "摄影"],
                "signature": "学而不思则罔，思而不学则殆"
            },
            {
                "username": "美食探索家",
                "email": "mstsj@example.com",
                "age": 28,
                "is_active": False,
                "registration_date": datetime.now(),
                "address": {
                    "provice": "四川省",
                    "city": "成都市",
                    "district": "锦江区"
                },
                "interests": ["美食", "烹饪"],
                "signature": "唯有美食与爱不可辜负"
            }
        ]
    )
def update_document(collection):
    collection.update_one(
        {"_id": {"$eq": 1}},
        {
            "$set": {
                "address.district": "黄岛区",
                "badges": "创作达人",
            },
            "$unset": {"interests": "",},
            "$currentDate": {"lastModified":True}
        }
    )
    collection.replace_one(
        {"username": {"$eq": "星空下的吉他"}},
        {"username": "星空下的吉他","age": 30},
    )
def delete_document(collection):
    collection.delete_one({"_id": {"$eq": 1}})
def find_document(collection):
    result = users.find(
        {},
        {
            "username": 1,
            "address.district": 1,
            "age": 1,
            "interests": 1,
            "badges": 1,
            "lastModified": 1
        }
    )
    for doc in result:
        print(doc)
if __name__ == '__main__':
    mongodbClient = mongodb_connect.MongoDBConnect.getConnect()
    pythonDatabase = mongodbClient.get_database("python_database")
    users = pythonDatabase.get_collection("users")
    insert_document(users)
    print("插入文档后查询集合users中的所有文档：")
    find_document(users)
    print("更新文档后查询集合users中的所有文档：")
    update_document(users)
    find_document(users)
    print("删除文档后查询集合users中的所有文档：")
    delete_document(users)
    find_document(users)

