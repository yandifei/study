package cn.itcast.mongodb;


// mongodb://username:password@host:port,host:port,.../?option&option&...
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
public class MongoDBConnect {
    private static final String URI = "mongodb://yandifei:yandifei@" +
            "127.0.0.1:27017/?authSource=admin";
    private static MongoClient mongoClient;
    public static MongoClient getConnection() {
        if (mongoClient == null) {
            mongoClient = MongoClients.create(URI);
        }
        return mongoClient;
    }
    public static void closeConnection() {
        if (mongoClient != null) {
            mongoClient.close();
            mongoClient = null;
        }
    }
}