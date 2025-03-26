package com.yandifei.objectpoly;

public class PolyObject {
    public static void main(String[] args) {

        //编译类型就是Animal，运行类型Dog
        Animal animal = new Dog();
        animal.cry();   //因为运行时，执行到改行时，animal运行类型是Dog，所以cry就是Dog的
        animal = new Cat();
        animal.cry();

        Object a = 1.00000;
        System.out.println(a);
    }
}
