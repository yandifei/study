package com.yandifei.extend_;
//大学生类-＞模拟大学生考试的考试情况
public class Graduate {
    public String name;
    public int age;
    private double score;   //成绩
    public void setScore(double score) {
        this.score = score;
    }

    public void testing() {
        System.out.println("大学生 " + name + " 正在考大学数学...");
    }

    public void showInfo() {
        System.out.println("大学生:" + name + " 年龄:" + age + " 分数:" + score);
    }
}
