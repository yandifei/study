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
UserService userService;
@Autowired
UserMapper userMapper;

    @Test
    void deleteUser() {
        int count=userMapper.deleteUser(1);//传递参数uid=2给接口
        if(count==0)
            System.out.println("删除数据失败");
        else
            System.out.println("删除了"+count+"条记录!");
    }

    @Test
    void updateUser() {
        User user=new User(); //创建一个对象，存放要添加的数据
        user.setUid(1);
        user.setUname("新数据2"); //给对象赋值
        user.setUage(23); //给对象赋值
        int count=userMapper.updateUser(user);//将user对象添加到表中，返回整数值, 0表示失败，大于0成功
        if(count==0)
            System.out.println("添加数据失败");
        else
            System.out.println("添加了"+count+"条记录!");
    }

    @Test
    void addUser() {
        User user=new User(); //创建一个对象，存放要添加的数据
        user.setUname("新数据1"); //给对象赋值
        user.setUage(23); //给对象赋值
        int count=userMapper.addUser(user);//将user对象添加到表中，返回整数值,0表示失败，大于0成功
        if(count==0)
            System.out.println("添加数据失败");
        else
            System.out.println("添加了"+count+"条记录!");
    }

    @Test
    void contextLoads() {
       User user=userService.findUserById(3);//ORM思想，把表的数据放到类的对象中
       System.out.println("用户名id："+user.getUid()+",用户名："+user.getUname()+",用户年龄："+user.getUage());
    }

    @Test
    void findUserAll() {
        List<User> userList=userService.findAllUser();
        //输出结果
        for(User user: userList){
            System.out.println("ID: " + user.getUid() + " 姓名: " + user.getUname()+" 年龄:"+user.getUage());
        }

    }

    @Test
    void findUserByName() {
        List<User> userList=userService.findUserByName("张");
        //输出结果
        for(User user: userList){
            System.out.println("ID: " + user.getUid() + " 姓名: " + user.getUname()+" 年龄:"+user.getUage());
        }

    }

    @Test
    public void findUser() {
        //传入参数查询，返回结果
        User user=new User();
        //user.setUid(2);
        //user.setUname("王国");
        //user.setUage(22);
        List<User> userList =userMapper.findUser(user);
        //输出结果
        for(User user2: userList){
            System.out.println("ID: " + user2.getUid() + " 姓名: " + user2.getUname()+" 年龄:"+user2.getUage());
        }
    }

}
