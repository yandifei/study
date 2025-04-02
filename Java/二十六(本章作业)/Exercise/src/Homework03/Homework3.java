package Homework03;

public class Homework3 {
    public static void main(String[] args) {
        Teacher teacher = new Teacher("小明",51,"老师", 50000);
        System.out.println(teacher.introduce());
    }
}

class Teacher {
    private String name;
    private int age;
    private String post;
    private double salary;

    public Teacher(String name, int age, String post, double salary) {
        this.name = name;
        this.age = age;
        this.post = post;
        this.salary = salary;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getPost() {
        return post;
    }

    public void setPost(String post) {
        this.post = post;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }


    public String introduce() {
        return "姓名:" + name + " 年龄:" + age + " 职称:" + post + "基本工资" + salary;
    }
}


class Professor extends Teacher {
    public Professor(String name, int age, String post) {
        super(name, age, post,1.3);
    }

    @Override
    public String introduce() {
        return super.introduce();
    }
}

class Professor2 extends Teacher {
    public Professor2(String name, int age, String post) {
        super(name, age, post,1.2);
    }

    @Override
    public String introduce() {
        return super.introduce();
    }
}

class Professor3 extends Teacher {
    public Professor3(String name, int age, String post) {
        super(name, age, post,1.1);
    }

    @Override
    public String introduce() {
        return super.introduce();
    }
}