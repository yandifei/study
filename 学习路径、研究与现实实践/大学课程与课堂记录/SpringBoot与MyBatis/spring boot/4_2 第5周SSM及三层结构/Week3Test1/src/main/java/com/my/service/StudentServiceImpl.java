package com.my.service;

import com.my.dao.StudentMapper;
import com.my.domain.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

// 通过注解让Spring管理
@Service
public class StudentServiceImpl implements StudentService {

    @Autowired
    private StudentMapper studentMapper;

    @Override
    public List<Student> findAllStudent() {
        System.out.println("Service层：查询所有学生信息");
        return studentMapper.findAllStudent();
    }

    @Override
    public List<Student> findStudentByName(String sname) {
        System.out.println("Service层：按姓名模糊查询学生，姓名关键字=" + sname);
        return studentMapper.findStudentByName(sname);
    }
}