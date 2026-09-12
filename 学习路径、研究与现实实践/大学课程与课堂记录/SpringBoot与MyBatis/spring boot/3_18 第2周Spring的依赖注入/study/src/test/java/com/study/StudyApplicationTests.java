package com.study;

import com.study.domain.Student;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class StudyApplicationTests {
    @Autowired
    @Qualifier("studentDomain")
    Student student;

    @Test
    void aaa() {
//        使用依赖
        student.setStucode("202302"); //给学号赋值
        student.setName("李四");//给姓名赋值
        student.setAge(18);//给年龄赋值
        System.out.println("学号"+student.getStucode()+"姓名:"+student.getName()+"年龄:"+student.getAge());

    }

    @Test
    void contextLoads() {
//        启动测试
        System.out.println("hello world!");

//        类和类方法测试
        Student student=new Student();//实例化对象student
        student.setStucode("202301"); //给学号赋值
        student.setName("张三");//给姓名赋值
        student.setAge(18);//给年龄赋值
//        System.out.println(student);
        System.out.println("学号"+student.getStucode()+"姓名:"+student.getName()+"年龄:"+student.getAge());
    }
}

