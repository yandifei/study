package com.my.service;

import com.my.domain.Student;
import com.my.pojo.TStudent;

import java.util.List;

public interface StudentService {
    public Student findStudent(String sname);

    //   新增通用学生查询方法
    public List<Student> findStudentDynamic(Student student);

//    动态增加学生
    public int addStudentDynamic(Student student);

    //  根据 sid 查询学生姓名、年龄及所有课程成绩
    public TStudent findStudentWithScoreById(int sid);
}
