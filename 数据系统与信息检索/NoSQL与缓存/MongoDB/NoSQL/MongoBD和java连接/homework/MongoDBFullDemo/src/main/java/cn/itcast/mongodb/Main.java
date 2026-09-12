package cn.itcast.mongodb;

public class Main {
    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println(" MongoDB Java 驱动程序完整实验案例");
        System.out.println("=========================================");

        try {
            System.out.println("\n【第一部分：数据库操作】");
            DatabaseDemo.demo();

            System.out.println("\n【第二部分：集合操作】");
            var db = MongoDBConnection.getDatabase("java_collection_demo");
            CollectionDemo.demo(db);

            System.out.println("\n【第三部分：文档操作】");
            var docDb = MongoDBConnection.getDatabase("java_document_demo");
            DocumentDemo.demo(docDb);

        } catch (Exception e) {
            System.err.println("❌ 发生错误：" + e.getMessage());
            e.printStackTrace();
        } finally {
            MongoDBConnection.close();
        }

        System.out.println("\n=========================================");
        System.out.println(" 实验完成！");
        System.out.println("=========================================");
    }
}