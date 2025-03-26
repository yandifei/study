package com.yandifei.override;
//2.编写一个Student类，继承Person类，增加id、score属性/private，以及构造 器，定义say方法（返回自我介绍的信息）
public class Student extends Person {
     private int id;
     private double score;

    public Student(String name, int age, int id, double score) {
        super(name, age);
        this.id = id;
        this.score = score;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    //say方法（返回自我介绍的信息）
    public String say() {
        return super.say() + " id：" + this.id +  " 分数" + this.score;
    }
}
