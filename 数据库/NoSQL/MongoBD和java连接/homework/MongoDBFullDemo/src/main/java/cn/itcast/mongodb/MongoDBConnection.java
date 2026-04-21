package cn.itcast.mongodb;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import com.mongodb.client.ListDatabasesIterable;

public class MongoDBConnection {
    private static final String CONNECTION_STRING =
            "mongodb://yandifei:yandifei@127.0.0.1:27017/?authSource=admin";
    private static MongoClient mongoClient = null;

    public static MongoClient getMongoClient() {
        if (mongoClient == null) {
            mongoClient = MongoClients.create(CONNECTION_STRING);
            System.out.println("✅ MongoDB连接成功！");
        }
        return mongoClient;
    }

    public static MongoDatabase getDatabase(String databaseName) {
        return getMongoClient().getDatabase(databaseName);
    }

    public static void close() {
        if (mongoClient != null) {
            mongoClient.close();
            mongoClient = null;
            System.out.println("🔌 MongoDB连接已关闭");
        }
    }

    public static void listDatabases() {
        ListDatabasesIterable<Document> databases = getMongoClient().listDatabases();
        System.out.println("📁 所有数据库列表：");
        for (Document db : databases) {
            System.out.println(" - " + db.getString("name"));
        }
    }
}