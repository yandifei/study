package com.study.service;

import com.study.entity.Users;

import java.util.List;

/**
 * 用户服务接口
 */
public interface UsersService {
    
    /**
     * 查询所有用户
     */
    List<Users> findAll();
    
    /**
     * 根据ID查询用户
     */
    Users findById(Integer uid);
    
    /**
     * 添加用户
     */
    int insert(Users users);
    
    /**
     * 更新用户
     */
    int update(Users users);
    
    /**
     * 删除用户
     */
    int delete(Integer uid);
}
