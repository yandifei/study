package com.yandifei.polymorphic;

public class Poly1 {
    public static void main(String[] args) {
        Master tom = new Master("汤姆");
        Dog dog = new Dog("大黄");
        Bone bone = new Bone("大棒骨");
        tom.feed(dog, bone);

        System.out.println("======================");

        Cat cat = new Cat("小花猫");
        Fish fish = new Fish("黄花鱼");
        tom.feed(cat, fish);
    }
}
