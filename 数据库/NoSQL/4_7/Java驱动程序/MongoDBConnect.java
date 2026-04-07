package cn.itcast.mongodb;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
public class MongoDBConnect {
    private static final String URI = "mongodb://itcastAdmin:123456@" +
            "192.168.121.134:27016/?authSource=admin";
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
