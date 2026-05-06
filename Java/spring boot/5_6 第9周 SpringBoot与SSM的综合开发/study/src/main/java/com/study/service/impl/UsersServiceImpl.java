package com.study.service.impl;

import com.study.entity.Users;
import com.study.mapper.UsersMapper;
import com.study.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 用户服务实现类
 */
@Service
public class UsersServiceImpl implements UsersService {
    
    @Autowired
    private UsersMapper usersMapper;
    
    @Override
    public List<Users> findAll() {
        return usersMapper.findAll();
    }
    
    @Override
    public Users findById(Integer uid) {
        return usersMapper.findById(uid);
    }
    
    @Override
    public int insert(Users users) {
        return usersMapper.insert(users);
    }
    
    @Override
    public int update(Users users) {
        return usersMapper.update(users);
    }
    
    @Override
    public int delete(Integer uid) {
        return usersMapper.delete(uid);
    }
}
