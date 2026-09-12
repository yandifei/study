package com.my.service;

import com.my.domain.User;
import org.apache.ibatis.annotations.Delete;

import java.util.List;

public interface UserService {
    public User findUserById(int uid);

    public List<User> findAllUser();
    public List<User> findUserByName(String uname);

    public int addUser(User user);
    public int updateUser(User user);
    public int deleteUser (int uid);

//    增加一个查询接口，这个是通用的查询接口
    public List<User> findUser(User user);
}
