import mongodb_connect

mongodbClient = mongodb_connect.MongoDBConnect.getConnect()
databaseNames = mongodbClient.list_database_names()
for name in databaseNames:
    print(name)
javaDatabase = mongodbClient.get_database("java_database")
mongodbClient.drop_database("java_database")
mongodbClient.close()
