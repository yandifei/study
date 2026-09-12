package com.study.homework;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class StudentClass {
    @Value("大数据22级1班")
    private String name;  //班级名称
    @Value("大数据系")
    private String department;   //系别
    @Value("45")
    private int num;  //班级人数

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public int getNum() {
        return num;
    }

    public void setNum(int num) {
        this.num = num;
    }

    @Override
    public String toString() {
        return "StudentClass{" +
                "name='" + name + '\'' +
                ", department='" + department + '\'' +
                ", num=" + num +
                '}';
    }
}
