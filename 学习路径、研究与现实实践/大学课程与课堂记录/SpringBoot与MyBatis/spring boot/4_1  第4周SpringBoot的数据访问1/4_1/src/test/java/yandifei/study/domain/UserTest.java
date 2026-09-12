package yandifei.study.domain;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import yandifei.study.dao.UserMapper;

import java.util.List;

// 必须添加SpringBootTest才能使用Autowired注解
@SpringBootTest
class UserTest {
    @Autowired
    UserMapper userMapper; //实例化接口

    @Test
    void  aaa() {
        User user=userMapper.findUserById(2);//调用接口的方法，读数据
        System.out.println("用户名id："+user.getUid()+",用户名："+user.getUname()+",用户年龄："+user.getUage());
        System.out.println(user); //输出数据
    }

    @Test
    void testUserAll() {
        List<User> userList = userMapper.findAllUser();
        //输出结果
        for(User user: userList){
            System.out.println("ID: " + user.getUid() + " 姓名: " + user.getUname()+" 年龄:"+user.getUage());
        }

    }
}