package com.yandifei.debug;

//debug对象创建的过程，加深对调试的理解
public class DebugExercise {
    public static void main(String[] args) {
        //创建对象的流程
        //(1)加载Person类信息
        //(2)初始化 2.1默认初始化，2.2显示初始化2.3构造器初始化
        //(3)返回对象的地址
        Person jack = new Person("jack", 20);
        System.out.println(jack);

    }
}

class Person {
    private String name;
    private int agej;

    public Person(String name, int agej) {
        this.name = name;
        this.agej = agej;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", agej=" + agej +
                '}';
    }
}