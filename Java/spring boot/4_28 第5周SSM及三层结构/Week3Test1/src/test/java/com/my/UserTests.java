package com.my;

import com.my.dao.UserMapper;
import com.my.domain.User;
import com.my.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Date;
import java.util.List;

@SpringBootTest
class UserTests {
    @Autowired
    // UserMapper userMapper;
    UserService userService;//这里改为Userservice对象

    @Test
    void aaa() {
        User user = userService.findUserById(2);
        System.out.println("用户名id：" + user.getUid() + ",用户名：" + user.getUname() + ",用户年龄：" + user.getUage());
    }

    @Test
    void testFindUserAll() {
        List<User> userList = userService.findAllUser();
        //输出结果
        for(User user: userList){
            System.out.println("ID: " + user.getUid() + " 姓名: " + user.getUname()+" 年龄:"+user.getUage());
        }
    }

    @Test
    void findUserByname() {
        //ORM思想，把表的数据放到类的对象中
        List<User> userList=userService.findUserByName("张");
        System.out.println(userList);
    }

//    @Test
//    void contextLoads() {
//       User user=userMapper.findUserById(3);//ORM思想，把表的数据放到类的对象中
//       System.out.println("用户名id："+user.getUid()+",用户名："+user.getUname()+",用户年龄："+user.getUage());
//    }
}
