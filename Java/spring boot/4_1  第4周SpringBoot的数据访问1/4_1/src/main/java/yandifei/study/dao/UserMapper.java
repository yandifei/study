package yandifei.study.dao;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import yandifei.study.domain.User;

import java.util.List;
@Mapper
public interface UserMapper {
//    @Select("select * from users where uid = #{uid}")
    public User findUserById(int uid);

//    @Select("select * from users")
    public List<User> findAllUser();
}
