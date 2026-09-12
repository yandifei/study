package com.yandifei.extend_.improve;

//父类,是Pupil 和 Graduate的父类
public class Student {
    public String name;
    public int age;
    private double score;   //成绩

    public void setScore(double score) {
        this.score = score;
    }

    public void showInfo() {
        System.out.println("学生名:" + name + " 年龄:" + age + " 分数:" + score);
    }
}
