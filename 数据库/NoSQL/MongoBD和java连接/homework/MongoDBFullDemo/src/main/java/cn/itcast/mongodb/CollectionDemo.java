package cn.itcast.mongodb;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.*;
import org.bson.Document;
import org.bson.conversions.Bson;
import java.util.Arrays;
import java.util.List;

public class CollectionDemo {

    public static void createCollection(MongoDatabase database, String collectionName) {
        System.out.println("\n========== 创建集合 ==========");
        try {
            database.createCollection(collectionName);
            System.out.println("✅ 创建集合成功：" + collectionName);
        } catch (Exception e) {
            System.out.println("⚠️ 集合可能已存在：" + e.getMessage());
        }
    }

    public static void createCappedCollection(MongoDatabase database, String collectionName,
                                              long sizeInBytes, long maxDocuments) {
        System.out.println("\n========== 创建固定大小集合 ==========");
        try {
            CreateCollectionOptions options = new CreateCollectionOptions()
                    .capped(true)
                    .sizeInBytes(sizeInBytes)
                    .maxDocuments(maxDocuments);
            database.createCollection(collectionName, options);
            System.out.println("✅ 创建固定大小集合成功：" + collectionName +
                    "（大小：" + sizeInBytes + "字节，最多：" + maxDocuments + "条）");
        } catch (Exception e) {
            System.out.println("⚠️ 创建失败：" + e.getMessage());
        }
    }

    public static void createView(MongoDatabase database, String viewName,
                                  String sourceCollection, List<Bson> pipeline) {
        System.out.println("\n========== 创建视图 ==========");
        try {
            database.createView(viewName, sourceCollection, pipeline);
            System.out.println("✅ 创建视图成功：" + viewName);
        } catch (Exception e) {
            System.out.println("⚠️ 创建视图失败：" + e.getMessage());
        }
    }

    public static void listCollections(MongoDatabase database) {
        System.out.println("\n========== 查看所有集合 ==========");
        System.out.println("数据库 [" + database.getName() + "] 中的集合列表：");
        for (String name : database.listCollectionNames()) {
            System.out.println(" 📄 " + name);
        }
    }

    public static MongoCollection<Document> getCollection(MongoDatabase database, String collectionName) {
        System.out.println("\n========== 访问集合 ==========");
        MongoCollection<Document> collection = database.getCollection(collectionName);
        System.out.println("✅ 已获取集合：" + collectionName);
        return collection;
    }

    public static void dropCollection(MongoDatabase database, String collectionName) {
        System.out.println("\n========== 删除集合 ==========");
        try {
            MongoCollection<Document> collection = database.getCollection(collectionName);
            collection.drop();
            System.out.println("🗑️ 集合 " + collectionName + " 已删除");
        } catch (Exception e) {
            System.out.println("❌ 删除失败：" + e.getMessage());
        }
    }

    public static void demo(MongoDatabase database) {
        createCollection(database, "users");
        createCappedCollection(database, "logs", 1048576, 1000);

        MongoCollection<Document> usersCollection = database.getCollection("users");
        usersCollection.insertOne(new Document("name", "张三").append("age", 25).append("year", 2024));
        usersCollection.insertOne(new Document("name", "李四").append("age", 30).append("year", 2024));
        usersCollection.insertOne(new Document("name", "王五").append("age", 28).append("year", 2023));

        List<Bson> pipeline = Arrays.asList(Aggregates.match(Filters.eq("year", 2024)));
        createView(database, "users_2024_view", "users", pipeline);

        listCollections(database);
        getCollection(database, "users");
        dropCollection(database, "users_2024_view");
        dropCollection(database, "logs");
        listCollections(database);
    }
}