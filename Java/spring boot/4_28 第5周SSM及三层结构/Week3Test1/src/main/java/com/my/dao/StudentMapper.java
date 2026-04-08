package com.my.dao;

import com.my.domain.Student;

import java.util.List;

public interface StudentMapper {

   public Student findStudent(String sname);

   // 查询所有学生
   public List<Student> findAllStudent();

   // 按姓名模糊查询
   public List<Student> findStudentByName(String sname);
}
