package com.my;

import org.junit.jupiter.api.Test;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Date;

@SpringBootTest
@MapperScan("com.my.dao")
class MyApplicationTests {

//    @Test
//    void contextLoads() {
//        Date date = new Date(); //获取当前时间
//        System.out.println(date);
//    }

//    主类测试
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
//    要改数据库配置文件application.properties
//    我用的是本机的,所以如果报错请该数据库用户和密码
//    访问  http://localhost:8080/finduser

//    访问：http://localhost:8080/inputuser
//    尝试只填姓名、只填年龄、都填、都不填（应至少填一项，否则SQL可能因字段列表为空而报错，实验中可以观察到动态效果）。

//    访问：http://localhost:8080/addstudent
//    姓名和年龄可选填，不填的字段将使用数据库默认值（NULL）

}

