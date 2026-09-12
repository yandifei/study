package yandifei.study.dao;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import yandifei.study.domain.Student;

@Mapper
public interface StudentMapper {
//    @Select("select * from t_student where sname = #{sname}")
    public Student findStudentBySname(String sname);
}
