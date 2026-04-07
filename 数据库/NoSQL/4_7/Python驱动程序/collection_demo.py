import mongodb_connect
mongodbClient = mongodb_connect.MongoDBConnect.getConnect()
pythonDatabase = mongodbClient.get_database("python_database")
pythonDatabase.create_collection("baseCollection")
pythonDatabase.create_collection(
    "cappedCollection",
    capped=True,
    size=5242880,
    max=5000
)
timeCollection = {
    "timeField":"timestamp",
    "metaField":"data",
    "granularity":"hours"
}
pythonDatabase.create_collection(
    "weather24h",
    timeseries=timeCollection,
    expireAfterSeconds=86400
)
clusteredCollection = {
    "key":{"_id":1},
    "unique":True,
    "name":"clusteredKey"
}
pythonDatabase.create_collection(
    "clusteredCollection",
    clusteredIndex=clusteredCollection
)
pythonDatabase.create_collection(
    "myView",
    viewOn="baseCollection",
    pipeline=[{"$match": { "year": 1 }}]
)
collections = pythonDatabase.list_collection_names()
for collection in collections:
    print(collection)
baseCollection = pythonDatabase.get_collection("baseCollection")
# 删除集合clusteredCollection
pythonDatabase.drop_collection("clusteredCollection")
mongodbClient.close()