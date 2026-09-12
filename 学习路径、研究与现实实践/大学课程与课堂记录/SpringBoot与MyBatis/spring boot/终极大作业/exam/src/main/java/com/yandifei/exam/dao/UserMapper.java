package com.yandifei.exam.dao;

import com.yandifei.exam.domain.Users;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 用户 Mapper 接口
 */
public interface UserMapper {

    // 根据 userCode 查询用户（用于登录验证）
    Users getUserByUserCode(@Param("userCode") String userCode);

    // 分页查询用户列表（带角色关联 + 条件搜索）
    List<Users> getUserListByPage(@Param("userName") String userName,
                                   @Param("userRole") Integer userRole);

    // 添加用户
    int add(Users user);

    // 根据 ID 查询用户
    Users getUserById(@Param("id") Integer id);

    // 修改用户
    int modify(Users user);

    // 删除用户
    int deleteUserById(@Param("id") Integer id);
}
