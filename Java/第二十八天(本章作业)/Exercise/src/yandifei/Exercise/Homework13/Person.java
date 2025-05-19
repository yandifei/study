package yandifei.Exercise.Homework13;

public class Person {
    private String name;
    private char sex;
    private int age;


    public Person(String name, char sex, int age) {
        this.name = name;
        this.sex = sex;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public char getSex() {
        return sex;
    }

    public void setSex(char sex) {
        this.sex = sex;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String play() {
         return "调用了父类的play方法";
    }

    public String basicInfo() {
        return "姓名: " + name + "\n年龄：" + age + "\n性别" + sex;
    }
}
