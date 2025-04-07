package yandifei.Exercise.Homework13;

public class Homework13 {
    public static void main(String[] args) {
        Teacher teacher = new Teacher("张飞", '男', 30, 5);
        Student student = new Student("小明", '男', 15, "00023102");


        //信息输出
        System.out.println("老师的信息:");
        System.out.println("姓名: " + teacher.getName());
        System.out.println("年龄: " + teacher.getAge());
        System.out.println("性别: " + teacher.getSex());
        System.out.println("工龄: " + teacher.getWork_age());
        System.out.println(teacher.play());
        System.out.println("-----------------------");
        System.out.println("学生的信息:");
        System.out.println("姓名: " + student.getName());
        System.out.println("年龄: " + student.getAge());
        System.out.println("性别: " + student.getSex());
        System.out.println("工龄: " + student.getStu_id());
        System.out.println(student.play());

    }
}
