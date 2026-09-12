package com.my.service;

import com.my.domain.User;

import java.util.List;

public interface UserService {
    public User findUserById(int uid);

    public List<User> findAllUser();

    public List<User> findUserByName(String uname);
}

