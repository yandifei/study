package com.yandifei.poly.Exercise;
//应用实例：判断两个Person对象的内容是否相等，如果两个Person对象的各个属性值都一样，则返回true,反之false。

public class EqualsExercise {
    public static void main(String[] args) {
        Person p1 = new Person("jack", 10, '男');
        Person p2 = new Person("tom", 20, '女');
        System.out.println(p1.equals(p1));


    }


}

class Person {
    private String name;
    private int age;
    private char gender;

    public Person(String name, int age, char gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
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

    public char getGender() {
        return gender;
    }

    public void setGender(char gender) {
        this.gender = gender;
    }

    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        //类型判断
        if(obj instanceof Person) { //是Person，我们才比较
            //进行向下转型，因为我需要得到obj的各个属性
            Person p = (Person)obj;
            return this.name.equals(p.name) && this.age == p.age && this.gender == p.gender;
        }

        return false;
    }
}