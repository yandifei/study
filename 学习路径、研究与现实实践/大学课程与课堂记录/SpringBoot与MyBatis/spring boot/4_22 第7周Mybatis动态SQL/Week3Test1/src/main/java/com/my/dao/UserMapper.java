package com.my.dao;

import com.my.domain.User;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface UserMapper {

    public User findUserById(int uid);

    public List<User> findAllUser();
    public List<User> findUserByName(String uname);

    public int addUser(User user);

    public int updateUser(User user);

    @Delete("delete from users where uid=#{uid}")
    public int deleteUser (int uid);

//    增加一个查询接口，这个是通用的查询接口
    public List<User> findUser(User user);
}
