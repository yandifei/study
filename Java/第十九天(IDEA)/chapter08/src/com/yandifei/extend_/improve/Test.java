package com.yandifei.extend_.improve;

import com.yandifei.extend_.Graduate;
import com.yandifei.extend_.Pupil;

public class Test {
    public static void main(String[] args) {
        com.yandifei.extend_.Pupil pupil = new Pupil();
        pupil.name = "小明";
        pupil.age = 11;
        pupil.testing();
        pupil.setScore(50);
        pupil.showInfo();
        System.out.println("=======================");
        com.yandifei.extend_.Graduate graduate = new Graduate();
        graduate.name = "金角大王";
        graduate.age = 22;
        graduate.testing();
        graduate.setScore(80);
        graduate.showInfo();
    }
}
