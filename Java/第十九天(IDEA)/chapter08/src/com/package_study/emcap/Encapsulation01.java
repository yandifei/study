package com.package_study.emcap;

public class Encapsulation01 {
    public static void main(String[] args) {
        Person person = new Person();
        person.setName("jack");
        person.setAge(30);
        person.setSalary(3000);
        System.out.println(person.info());
        //创建一个有参对象
        System.out.println("=================");
        Person person1 = new Person("yan",100,1000);
        System.out.println(person1.info());


    }
}
/*
那么在java中如何实现这种类似的控制呢?
请大家看一个小程序(com.hspedu.encap：Encapsulationo1。java),
不能随便查看人的年龄，工资等隐私，并对设置的年龄进行合理的验证。年龄合理就设置，否则给默认
年龄，必须在1-120，年龄，工资不能直接查看，name的长度在 2-6字符之间
 */
class Person {
    public String name; //名字公开
    private int age;    //age私有化
    private double salary; //..

    //构造器alt + insert
    public Person() {
    }

    public Person(String name, int age, double salary) {
//        this.name = name;
//        this.age = age;
//        this.salary = salary;
        //我们可以将set方法写在构造器中，这样仍然可以验证
        setName(name);
        setAge(age);
        setSalary(salary);
    }
    /*自己写getXxx和setXxx太慢了，我们使用快捷键alt + insert
    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }*/

    //根据要求完善代码
    public String getName() {
        return name;
    }

    public void setName(String name) {
        //加入对数据的校验，相当于增加业务逻辑
        if(name.length() >= 2 && name.length() <= 6) {
            this.name = name;
        } else {
            System.out.println("名字的长度不对，需要(2-6)个字符，默认名字“无名小子”");
            this.name = "无名人";
        }
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if(age >= 1 && age <= 120) {
            this.age = age;
        } else {
            System.out.println("年龄需要在（1-120），默认年龄18");
            this.age = 18;  //给一个默认年龄
        }
    }

    public double getSalary() {
        //可以增加对当前对象的权限判断
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    //写一个方法，返回属性信息
    public String info() {
        return "信息为 name=" + name + " age=" + age + " 薪水=" + salary;
    }
}
