package com.yandifei.exam.service;

import com.yandifei.exam.domain.Users;

import java.util.List;

/**
 * 用户 Service 接口
 */
public interface UserService {

    // 登录验证
    Users login(String userCode, String userPassword);

    // 根据 userCode 查询用户
    Users getUserByUserCode(String userCode);

    // 分页查询用户列表
    List<Users> getUserListByPage(String queryUserName, Integer queryUserRole);

    // 添加用户
    boolean add(Users user);

    // 根据 ID 查询用户
    Users getUserById(Integer id);

    // 修改用户
    boolean modify(Users user);

    // 删除用户
    boolean deleteUserById(Integer id);
}
