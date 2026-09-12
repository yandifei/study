package com.sang;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest   // 启动 Spring 应用上下文，测试整个应用是否能加载
public class AppTest {

    @Test
    public void contextLoads() {
        System.out.println("测试运行成功！");
    }
}