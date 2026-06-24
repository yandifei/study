package com.yandifei.exam.service.impl;

import com.yandifei.exam.dao.UserMapper;
import com.yandifei.exam.domain.Users;
import com.yandifei.exam.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 用户 Service 实现
 */
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Override
    public Users login(String userCode, String userPassword) {
        Users user = userMapper.getUserByUserCode(userCode);
        if (user != null && user.getUserPassword().equals(userPassword)) {
            return user;
        }
        return null;
    }

    @Override
    public Users getUserByUserCode(String userCode) {
        return userMapper.getUserByUserCode(userCode);
    }

    @Override
    public List<Users> getUserListByPage(String queryUserName, Integer queryUserRole) {
        return userMapper.getUserListByPage(queryUserName, queryUserRole);
    }

    @Override
    public boolean add(Users user) {
        return userMapper.add(user) > 0;
    }

    @Override
    public Users getUserById(Integer id) {
        return userMapper.getUserById(id);
    }

    @Override
    public boolean modify(Users user) {
        return userMapper.modify(user) > 0;
    }

    @Override
    public boolean deleteUserById(Integer id) {
        return userMapper.deleteUserById(id) > 0;
    }
}
