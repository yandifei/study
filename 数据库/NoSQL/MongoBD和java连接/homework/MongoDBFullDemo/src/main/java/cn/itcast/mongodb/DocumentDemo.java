package cn.itcast.mongodb;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.*;
import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.InsertManyResult;
import com.mongodb.client.result.InsertOneResult;
import com.mongodb.client.result.UpdateResult;
import org.bson.Document;
import org.bson.conversions.Bson;
import java.util.Arrays;
import java.util.List;

public class DocumentDemo {

    public static void insertOne(MongoCollection<Document> collection, Document doc) {
        System.out.println("\n========== 插入单个文档 ==========");
        InsertOneResult result = collection.insertOne(doc);
        System.out.println("✅ 插入成功！文档ID：" + result.getInsertedId().asObjectId().getValue());
    }

    public static void insertMany(MongoCollection<Document> collection, List<Document> docs) {
        System.out.println("\n========== 插入多个文档 ==========");
        InsertManyResult result = collection.insertMany(docs);
        System.out.println("✅ 批量插入成功！共插入 " + docs.size() + " 条文档");
    }

    public static void findAll(MongoCollection<Document> collection) {
        System.out.println("\n========== 查询所有文档 ==========");
        for (Document doc : collection.find()) {
            System.out.println(" 📄 " + doc.toJson());
        }
    }

    public static void findByFilter(MongoCollection<Document> collection, String field, Object value) {
        System.out.println("\n========== 条件查询： " + field + " = " + value + " ==========");
        Bson filter = Filters.eq(field, value);
        for (Document doc : collection.find(filter)) {
            System.out.println(" 📄 " + doc.toJson());
        }
    }

    public static void findByRange(MongoCollection<Document> collection) {
        System.out.println("\n========== 范围查询：age >= 25 ==========");
        Bson filter = Filters.gte("age", 25);
        for (Document doc : collection.find(filter)) {
            System.out.println(" 📄 " + doc.toJson());
        }
    }

    public static void findByPage(MongoCollection<Document> collection, int skip, int limit) {
        System.out.println("\n========== 分页查询：跳过 " + skip + " 条，显示 " + limit + " 条 ==========");
        for (Document doc : collection.find().skip(skip).limit(limit)) {
            System.out.println(" 📄 " + doc.toJson());
        }
    }

    public static void findBySort(MongoCollection<Document> collection, String field, int order) {
        System.out.println("\n========== 排序查询：按 " + field + " " + (order == 1 ? "升序" : "降序") + " ==========");
        Bson sort = Sorts.orderBy(Sorts.orderBy(new Document(field, order)));
        for (Document doc : collection.find().sort(sort)) {
            System.out.println(" 📄 " + doc.toJson());
        }
    }

    public static void updateOne(MongoCollection<Document> collection, Bson filter, Bson update) {
        System.out.println("\n========== 更新单个文档 ==========");
        UpdateResult result = collection.updateOne(filter, update);
        System.out.println("✅ 匹配到 " + result.getMatchedCount() + " 条，修改了 " + result.getModifiedCount() + " 条");
    }

    public static void updateMany(MongoCollection<Document> collection, Bson filter, Bson update) {
        System.out.println("\n========== 更新多个文档 ==========");
        UpdateResult result = collection.updateMany(filter, update);
        System.out.println("✅ 匹配到 " + result.getMatchedCount() + " 条，修改了 " + result.getModifiedCount() + " 条");
    }

    public static void replaceOne(MongoCollection<Document> collection, Bson filter, Document replacement) {
        System.out.println("\n========== 替换文档 ==========");
        UpdateResult result = collection.replaceOne(filter, replacement);
        System.out.println("✅ 替换了 " + result.getModifiedCount() + " 条文档");
    }

    public static void deleteOne(MongoCollection<Document> collection, Bson filter) {
        System.out.println("\n========== 删除单个文档 ==========");
        DeleteResult result = collection.deleteOne(filter);
        System.out.println("✅ 删除了 " + result.getDeletedCount() + " 条文档");
    }

    public static void deleteMany(MongoCollection<Document> collection, Bson filter) {
        System.out.println("\n========== 删除多个文档 ==========");
        DeleteResult result = collection.deleteMany(filter);
        System.out.println("✅ 删除了 " + result.getDeletedCount() + " 条文档");
    }

    public static void demo(MongoDatabase database) {
        MongoCollection<Document> collection = database.getCollection("users");
        collection.drop();
        database.createCollection("users");
        collection = database.getCollection("users");

        Document user1 = new Document("name", "张三")
                .append("age", 25)
                .append("email", "zhangsan@example.com")
                .append("city", "北京");
        insertOne(collection, user1);

        List<Document> users = Arrays.asList(
                new Document("name", "李四").append("age", 30).append("email", "lisi@example.com").append("city", "上海"),
                new Document("name", "王五").append("age", 28).append("email", "wangwu@example.com").append("city", "广州"),
                new Document("name", "赵六").append("age", 22).append("email", "zhaoliu@example.com").append("city", "深圳"),
                new Document("name", "小明").append("age", 35).append("email", "xiaoming@example.com").append("city", "北京")
        );
        insertMany(collection, users);

        findAll(collection);
        findByFilter(collection, "city", "北京");
        findByRange(collection);
        findByPage(collection, 0, 3);
        findBySort(collection, "age", 1);

        updateOne(collection, Filters.eq("name", "张三"), Updates.set("age", 26));
        updateMany(collection, Filters.eq("city", "北京"), Updates.set("city", "首都"));

        Document newWangwu = new Document("name", "王五")
                .append("age", 29)
                .append("email", "wangwu_new@example.com")
                .append("city", "深圳")
                .append("phone", "13800138000");
        replaceOne(collection, Filters.eq("name", "王五"), newWangwu);

        System.out.println("\n========== 更新后的数据 ==========");
        findAll(collection);

        deleteOne(collection, Filters.eq("age", 22));
        deleteMany(collection, Filters.gt("age", 30));

        System.out.println("\n========== 删除后的数据 ==========");
        findAll(collection);
    }
}