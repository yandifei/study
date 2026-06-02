package cn.itcast.mongodb;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import java.util.*;
public class InsertDocumentDemo {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoDBConnect.getConnection();
        //访问数据库java_database
        MongoDatabase myDatabase =
                mongoClient.getDatabase("java_database");
        //访问集合users
        MongoCollection<Document> users
                = myDatabase.getCollection("users");
        HashMap<String, Object> docMap = new HashMap<>();
        docMap.put("username","星空下的吉他");
        docMap.put("email","xkxdjt@example.com");
        docMap.put("age",30);
        docMap.put("is_active",false);
        docMap.put("registration_date",new Date());
        docMap.put("address",new Document("provice", "广东省")
                .append("city", "广州市")
                .append("district", "天河区")
        );
        docMap.put("interests",Arrays.asList("音乐", "吉他"));
        docMap.put("signature","音乐是灵魂的语言");
        Document doc1 = new Document("_id", 1)
                .append("username", "追梦赤子心")
                .append("email", "zmczx@example.com")
                .append("age",30)
                .append("is_active", true)
                .append("registration_date", new Date())
                .append("address",
                        new Document("provice", "山东省")
                                .append("city", "青岛市")
                                .append("district", "崂山区")
                )
                .append("interests", Arrays.asList("读书", "旅行", "摄影"))
                .append("signature", "学而不思则罔，思而不学则殆");
        Document doc2 = new Document(docMap);
        Document doc3 = new Document("username", "美食探索家")
                .append("email", "mstsj@example.com")
                .append("age",28)
                .append("is_active", false)
                .append("registration_date", new Date())
                .append("address",
                        new Document("provice", "四川省")
                                .append("city", "成都市")
                                .append("district", "锦江区")
                )
                .append("interests", Arrays.asList("美食", "烹饪"))
                .append("signature", "唯有美食与爱不可辜负");
        List<Document> docList = Arrays.asList(doc2, doc3);
        users.insertOne(doc1);
        users.insertMany(docList);
        MongoDBConnect.closeConnection();
    }
}
