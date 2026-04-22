package com.my.service;

import com.my.dao.StudentMapper;
import com.my.domain.Student;
import com.my.domain.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

// 这个是新建的类，我来给他具体实现，这节课的核心是findStudentDynamic方法，动态sql

@Service
public class StudentServiceImpl implements StudentService {
    @Autowired
    private StudentMapper studentMapper;

    @Override
    public Student findStudent(String sname) {
        return studentMapper.findStudent(sname);
    }

    @Override
    public List<Student> findStudentDynamic(Student student) {
        return studentMapper.findStudentDynamic(student);
    }

    @Override
    public int addStudentDynamic(Student student) {
        return studentMapper.addStudentDynamic(student);
    }
}