package com.yandifei.poly.polyarr;

public class Teacher extends Person {
    private double salary;

    public Teacher(int age, String name, double salary) {
        super(age, name);
        this.salary = salary;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    public String say() {
        return  super.say() + " 薪水:" + this.salary;
    }
}
