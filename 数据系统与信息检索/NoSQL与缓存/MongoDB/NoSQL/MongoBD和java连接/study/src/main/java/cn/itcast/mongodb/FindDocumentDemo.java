package cn.itcast.mongodb;

import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Projections;
import org.bson.Document;
import org.bson.conversions.Bson;
import static com.mongodb.client.model.Indexes.descending;
public class FindDocumentDemo {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoDBConnect.getConnection();
        //访问数据库my_database
        MongoDatabase myDatabase =
                mongoClient.getDatabase("java_database");
        //访问集合users，该集合为3.3.5节创建
        MongoCollection<Document> users
                = myDatabase.getCollection("users");
        Bson andFilter =
                Filters.and(
                        Filters.gte("age", 20),
                        Filters.lte("age", 25)
                );
        Bson allFilter =
                Filters.all("interests", new String[]{"美食", "烹饪"});
        Bson include = Projections.fields(
                Projections.include("username", "age", "address.province"),
                Projections.excludeId()
        );
        FindIterable<Document> result1 =
                users.find(andFilter).projection(include);
        FindIterable<Document> result2 = users.find(allFilter);
        FindIterable<Document> result3 =
                users.find().projection(include)
                        .sort(descending("age")).limit(2);
        System.out.println("result1的查询结果：");
        for (Document document : result1){
            System.out.println(document);
        }
        System.out.println("result2的查询结果：");
        for (Document document : result2){
            System.out.println(
                    document.get("username") +
                            "\t" +
                            document.get("interests")
            );
        }
        System.out.println("result3的查询结果：");
        for (Document document : result3){
            System.out.println(document);
        }
        MongoDBConnect.closeConnection();
    }
}