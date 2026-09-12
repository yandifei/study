package com.study;

import com.study.homework.Book;
import com.study.homework.Student;
import com.study.homework.StudentClass;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class MyTests {
    @Autowired
    @Qualifier("studentHomework")
//  我有2个student对象，所以要用@Qualifier指定
    Student student;
    @Autowired
    Book book;


    @Test
    void test1() {
//        使用依赖就不用下面的set方法设置属性了,直接注入属性
//        StudentClass studentClass=new StudentClass();
//        studentClass.setName("大数据22级1班");
//        studentClass.setDepartment("大数据系");
//        studentClass.setNum(45);
//        student.setStudentClass(studentClass); //这里将班级对象赋给Student对象
        System.out.println("学号"+student.getStucode()+"\t姓名:"+student.getName()+"\t年龄:"+student.getAge());
        System.out.println(book);
    }
}
