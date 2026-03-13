package com.homework.controller;

import com.homework.mypack.Myear;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    @GetMapping("")
    public String isLeapYear() {
        Myear myear=new Myear();
        return "2026年是否是闰年：" + myear.isLeapYear(2026);

    }
}
