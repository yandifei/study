package com.yandifei.poly.polyarr;

public class Student extends Person {
    private double score;

    public Student(int age, String name, double score) {
        super(age, name);
        this.score = score;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public String say() {
        return super.say() + " 成绩:" + this.score;
    }
}
