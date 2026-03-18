package com.homework.utils;

public class TestCircle {
    // 测试方法
    public static void main(String[] args) {
        Circle circle = new Circle(5.0);
        System.out.println("半径: " + circle.getR());
        System.out.println("面积: " + circle.area());
        System.out.println("周长: " + circle.perimeter());
    }
}
