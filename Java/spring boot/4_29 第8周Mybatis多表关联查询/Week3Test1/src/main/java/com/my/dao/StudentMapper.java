package com.my.dao;

import com.my.domain.Student;
import com.my.pojo.TStudent;

import java.util.List;

public interface StudentMapper {

   public Student findStudent(String sname);

//   新增通用学生查询方法
   public List<Student> findStudentDynamic(Student student);


//   sql动态语句增加学生
   public int addStudentDynamic(Student student);

   // sql动态语句查询学生
   public TStudent findStudentWithScoreById(int sid);

}
