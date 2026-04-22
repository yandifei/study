package com.my.dao;

import com.my.domain.User;
import org.apache.ibatis.annotations.Select;

import java.util.List;


public interface UserMapper {
//    2个方式去定义，但是不能2个都要，不然抢id
//    @Select("select * from users where uid=#{uid}")
    public User findUserById(int uid);

    public List<User> findAllUser();

    public List<User> findUserByName(String uname);

}
