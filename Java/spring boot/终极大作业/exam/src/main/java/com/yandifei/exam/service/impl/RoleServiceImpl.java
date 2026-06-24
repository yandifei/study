package com.yandifei.exam.service.impl;

import com.yandifei.exam.dao.RoleMapper;
import com.yandifei.exam.domain.SmbmsRole;
import com.yandifei.exam.service.RoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 角色 Service 实现
 */
@Service
public class RoleServiceImpl implements RoleService {

    @Autowired
    private RoleMapper roleMapper;

    @Override
    public List<SmbmsRole> getRoleList() {
        return roleMapper.getBySmbmsRole();
    }
}
