package com.my.service;

import com.my.domain.Student;
import com.my.service.StudentService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
public class StudentServiceImplTest {
    @Autowired
    private StudentService studentService;

    @Test
    public void testDynamicQuery() {
        Student student = new Student();
        // 取消注释进行测试
        // student.setSid(2);
        // student.setSname("L");
        // student.setSage(20);

        List<Student> list = studentService.findStudentDynamic(student);
        for (Student s : list) {
            System.out.println(s);
        }
    }
}