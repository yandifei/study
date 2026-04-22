package com.my.service;

import com.my.dao.UserMapper;
import com.my.domain.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service    //别忘了里这
public class UserServiceImpl implements UserService {
    @Autowired
    UserMapper userMapper; //实例化接口

    @Override
    public User findUserById(int uid) {

            System.out.println("你要查的id=" + uid);
            return userMapper.findUserById(uid);
           }

    @Override
    public List<User> findAllUser(){
        System.out.println("以下是全部用户数据:");
        return userMapper.findAllUser();

    }

    @Override
    public List<User> findUserByName(String uname) {
        System.out.println("你要查的姓名是:"+uname);
        return userMapper.findUserByName(uname);
    }

    @Override
    public int addUser(User user) {
       return userMapper.addUser(user);
    }

    @Override
    public int updateUser(User user) {
        return userMapper.updateUser(user);
    }

    @Override
    public int deleteUser(int uid) {
        return userMapper.deleteUser(uid);
    }

//    具体是实现这个接口
    @Override
    public List<User> findUser(User user) {
        return  userMapper.findUser(user);
    }

}
