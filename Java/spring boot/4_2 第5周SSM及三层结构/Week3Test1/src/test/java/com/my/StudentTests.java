package com.my;

import com.my.dao.StudentMapper;
import com.my.dao.UserMapper;
import com.my.domain.Student;
import com.my.domain.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class StudentTests {
@Autowired
    StudentMapper studentMapper;

    @Test
    void contextLoads() {
       Student student=studentMapper.findStudent("Lili");//ORM思想，把表的数据放到类的对象中
       System.out.println(student);
    }


}
