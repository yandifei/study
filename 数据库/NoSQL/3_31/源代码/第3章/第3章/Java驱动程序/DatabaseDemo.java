package cn.itcast.mongodb;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;
public class DatabaseDemo {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoDBConnect.getConnection();
        MongoIterable<String> databaseNames1 =
                mongoClient.listDatabaseNames();
        System.out.println("MongoDB包含的所有非空数据库（删除数据库前）");
        for (String databaseName : databaseNames1){
            System.out.println(databaseName);
        }
        MongoDatabase testDatabase =
                mongoClient.getDatabase("test_database");
        testDatabase.drop();
        MongoIterable<String> databaseNames2 =
                mongoClient.listDatabaseNames();
        System.out.println("MongoDB包含的所有非空数据库（删除数据库后）");
        for (String databaseName : databaseNames2){
            System.out.println(databaseName);
        }
        MongoDBConnect.closeConnection();
    }
}
