package com.yandifei.override;
//编写一个Person类，包括属性/private(name、age），构造器、方法say(返回自我介绍的字符串）。
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
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

    //say(返回自我介绍的字符串）
    public String say() {
        return "我的名字是" + this.name + " 我的年龄是" + this.age;
    }

}
