package com.study.mapper;

import com.study.entity.Users;
import org.apache.ibatis.annotations.*;

import java.util.List;

/**
 * 用户Mapper接口
 */
@Mapper
public interface UsersMapper {
    
    /**
     * 查询所有用户
     */
    @Select("SELECT * FROM users")
    List<Users> findAll();
    
    /**
     * 根据ID查询用户
     */
    @Select("SELECT * FROM users WHERE uid = #{uid}")
    Users findById(Integer uid);
    
    /**
     * 添加用户
     */
    @Insert("INSERT INTO users(uname, uage) VALUES(#{uname}, #{uage})")
    @Options(useGeneratedKeys = true, keyProperty = "uid")
    int insert(Users users);
    
    /**
     * 更新用户
     */
    @Update("UPDATE users SET uname=#{uname}, uage=#{uage} WHERE uid=#{uid}")
    int update(Users users);
    
    /**
     * 删除用户
     */
    @Delete("DELETE FROM users WHERE uid=#{uid}")
    int delete(Integer uid);
}
