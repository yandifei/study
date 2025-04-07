package yandifei.Exercise.Homework11;

public class Homework11 {
    public static void main(String[] args) {
        // 测试test
        Person person = new Student("学生"); //向上转型
        person.run();
        person.eat();


        //向下转型
        Student person1 = (Student)person;
        person1.run();
        person1.eat();
        person1.study();


    }
}
