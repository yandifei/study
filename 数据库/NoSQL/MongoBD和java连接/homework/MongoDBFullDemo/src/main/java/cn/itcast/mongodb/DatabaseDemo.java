package cn.itcast.mongodb;

import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;

public class DatabaseDemo {

    public static void showAllDatabases() {
        System.out.println("\n========== 查看所有数据库 ==========");
        MongoIterable<String> databaseNames = MongoDBConnection.getMongoClient().listDatabaseNames();
        System.out.println("数据库列表：");
        for (String name : databaseNames) {
            System.out.println(" 📁 " + name);
        }
    }

    public static MongoDatabase accessDatabase(String dbName) {
        System.out.println("\n========== 访问数据库 ==========");
        MongoDatabase database = MongoDBConnection.getDatabase(dbName);
        System.out.println("✅ 已获取数据库：" + dbName);
        return database;
    }

    public static void dropDatabase(String dbName) {
        System.out.println("\n========== 删除数据库 ==========");
        MongoDatabase database = MongoDBConnection.getDatabase(dbName);
        try {
            database.drop();
            System.out.println("🗑️ 数据库 " + dbName + " 已删除");
        } catch (Exception e) {
            System.out.println("❌ 删除失败：" + e.getMessage());
        }
    }

    public static void demo() {
        showAllDatabases();
        MongoDatabase db = accessDatabase("java_test_db");
        db.createCollection("test_collection");
        System.out.println("✅ 已在 " + db.getName() + " 数据库中创建测试集合");
        showAllDatabases();
        dropDatabase("java_test_db");
        showAllDatabases();
    }
}