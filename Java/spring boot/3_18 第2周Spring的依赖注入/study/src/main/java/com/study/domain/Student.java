package com.study.domain;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component("studentDomain")
@ConfigurationProperties(prefix = "student")
public class Student {
//    @Value("202203")
    private String stucode;
//    @Value("王五")
    private String name;
//    @Value("19")
    private int age;

    public String getStucode() {
        return stucode;
    }

    public void setStucode(String stucode) {
        this.stucode = stucode;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "Student{" +
                "stucode='" + stucode + '\'' +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
}
