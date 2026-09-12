package cn.itcast.mongodb;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;
import org.bson.Document;
import org.bson.conversions.Bson;
public class UpdateDocumentDemo {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoDBConnect.getConnection();
        //访问数据库java_database
        MongoDatabase myDatabase =
                mongoClient.getDatabase("java_database");
        //访问集合users
        MongoCollection<Document> users= myDatabase.getCollection("users");
        Bson eqFilter1 = Filters.eq("_id", 1);
        Bson setUpdate1 = Updates.set("address.district", "黄岛区");
        Bson setUpdate2 = Updates.set("badges", "创作达人");
        Bson currentDate = Updates.currentDate("lastModified");
        Bson unsetUpdate = Updates.unset("interests");
        users.updateOne(eqFilter1,setUpdate1);
        users.updateOne(eqFilter1,setUpdate2);
        users.updateOne(eqFilter1,currentDate);
        users.updateOne(eqFilter1,unsetUpdate);
        Bson eqFilter2 = Filters.eq("is_active", false);
        Bson setUpdate3 = Updates.set("is_active", true);
        users.updateMany(eqFilter2,setUpdate3);
        Bson eqFilter3 = Filters.eq("username", "星空下的吉他");
        Document doc =
                new Document("username", "星空下的吉他").append("age", 30);
        users.replaceOne(eqFilter3,doc);
        MongoDBConnect.closeConnection();
    }
}
