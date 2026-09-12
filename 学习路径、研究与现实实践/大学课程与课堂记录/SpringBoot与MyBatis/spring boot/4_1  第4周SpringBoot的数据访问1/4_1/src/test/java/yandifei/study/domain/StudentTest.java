package yandifei.study.domain;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import yandifei.study.dao.StudentMapper;

@SpringBootTest
public class StudentTest {
    @Autowired
    StudentMapper studentMapper; //实例化接口

    @Test
    void testFindStudentBySname() {
        Student student = studentMapper.findStudentBySname("Lili");
        student.toString();
    }
}
