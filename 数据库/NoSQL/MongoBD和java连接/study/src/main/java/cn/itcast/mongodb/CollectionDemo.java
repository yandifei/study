package cn.itcast.mongodb;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.*;
import org.bson.Document;
import org.bson.conversions.Bson;
import java.util.Arrays;
import java.util.List;
public class CollectionDemo {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoDBConnect.getConnection();
        //访问数据库java_database
        MongoDatabase javaDatabase =
                mongoClient.getDatabase("java_database");
        //创建基础集合baseCollection
        javaDatabase.createCollection("baseCollection");
        javaDatabase.createCollection("cappedCollection",
                new CreateCollectionOptions()
                        .capped(true)
                        .sizeInBytes(5242880)
                        .maxDocuments(5000)
        );
        javaDatabase.createCollection("weather24h",
                new CreateCollectionOptions()
                        .timeSeriesOptions(
                                new TimeSeriesOptions("timestamp")
                                        .metaField("data")
                                        .granularity(TimeSeriesGranularity.HOURS)
                        )
        );
        Document document = new Document("_id", 1);
        javaDatabase.createCollection("clusteredCollection",
                new CreateCollectionOptions()
                        .clusteredIndexOptions(
                                new ClusteredIndexOptions(document,true)
                                        .name("clusteredKey")
                        )
        );
        List<Bson> list = Arrays.asList(
                Aggregates.match(Filters.eq("year", 1))
        );
        javaDatabase.createView("myView","baseCollection",list);
        System.out.println("数据库java_database中的所有集合（删除集合前）");
        for (String collectionName : javaDatabase.listCollectionNames()) {
            System.out.println(collectionName);
        }
        MongoCollection<Document> clusteredCollection =
                javaDatabase.getCollection("clusteredCollection");
        clusteredCollection.drop();
        System.out.println("数据库java_database中的所有集合（删除集合后）");
        for (String collectionName : javaDatabase.listCollectionNames()) {
            System.out.println(collectionName);
        }
        MongoDBConnect.closeConnection();
    }
}