package com.homework.utils;

public class Circle {
    // 属性：半径
    private double r;

    // 构造方法
    public Circle() {
    }

    public Circle(double r) {
        this.r = r;
    }

    // getter 和 setter 方法
    public double getR() {
        return r;
    }

    public void setR(double r) {
        this.r = r;
    }

    // 计算面积
    public double area() {
        return Math.PI * r * r;
    }

    // 计算周长
    public double perimeter() {
        return 2 * Math.PI * r;
    }
}
