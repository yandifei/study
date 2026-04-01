package com.my;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Date;

@SpringBootTest
class MyApplicationTests {

    @Test
    void contextLoads() {
        Date date = new Date(); //获取当前时间
        System.out.println(date);
    }

}
