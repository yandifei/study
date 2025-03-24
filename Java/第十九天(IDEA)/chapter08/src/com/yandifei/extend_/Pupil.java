package com.yandifei.extend_;

import com.sun.xml.internal.ws.addressing.WsaActionUtil;

//小学生->模拟小学生考试的情况
public class Pupil {
    public String name;
    public int age;
    private double score;   //成绩

    public void setScore(double score) {
        this.score = score;
    }

    public void testing() {
        System.out.println("小学生 " + name + " 正在考小学数学...");
    }

    public void showInfo() {
        System.out.println("小学生:" + name + " 年龄:" + age + " 分数:" + score);
    }
}
