package com.my.service;

import com.my.domain.Student;
import java.util.List;

public interface StudentService {
    List<Student> findAllStudent();
    List<Student> findStudentByName(String sname);
}