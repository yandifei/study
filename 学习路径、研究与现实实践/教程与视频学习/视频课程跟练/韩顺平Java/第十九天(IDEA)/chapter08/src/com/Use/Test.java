package com.Use;

import com.yandifei.Dog;

public class Test {
    public static void main(String[] args) {
        Dog dog = new Dog();    //其实这个Dog = com.yandifei.Dog
        System.out.println(dog);
        com.xiaoming.Dog dog1 = new com.xiaoming.Dog(); //自带包名
        System.out.println(dog1);
    }
}
