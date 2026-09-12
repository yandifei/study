package cn.itcast.mongodb;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import org.bson.Document;
import org.bson.conversions.Bson;
public class DeleteDocumentDemo {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoDBConnect.getConnection();
        //访问数据库java_database
        MongoDatabase myDatabase =
                mongoClient.getDatabase("java_database");
        //访问集合users
        MongoCollection<Document> users
                = myDatabase.getCollection("users");
        Bson eqFilter1 = Filters.eq("username", "美食探索家");
        users.deleteOne(eqFilter1);
        Bson eqFilter2 = Filters.eq("age", 30);
        users.deleteMany(eqFilter2);
        MongoDBConnect.closeConnection();
    }
}
