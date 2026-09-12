package com.my.controller;

import org.springframework.context.annotation.Conditional;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpServletRequest;
import java.util.Date;


@Controller
public class MyController {

    @GetMapping("/page1")
    public String page1(Model model){
        int a,b,c;
        a=27;b=31; //给a,b赋值
        c=a*b; //简单进行一个四则运算
        Date date = new Date(); //获取当前时间
        model.addAttribute("cValue", c);//把c的值放到cValue这个变量里
        model.addAttribute("nowTime",date); //把date的值放到nowtime这个变量里
        return "aaa.html";
    }

    @GetMapping("/input")
    public String input(){
        return "input.html";
    }

//    @GetMapping(value = "/getValue")
//    public String getValue(HttpServletRequest request, Model model){
//        String t1,t2;
//        t1=request.getParameter("text1");//获取前端的name是text1控件的值
//        t2=request.getParameter("text2");//获取前端的name是text2控件的值
//        Double a,b,c;
//        a=Double.parseDouble(t1) ;  //将t1转为double型变量,赋给a
//        b=Double.parseDouble(t2);  //将t2转为double型变量,赋给b
//        c=a*b;  //计算结果
//        System.out.println(t1+"-"+t2);
//        model.addAttribute("cValue",c);
//        return "input.html";
//    }

    @PostMapping(value = "/getValue")
    public String getValue(@RequestParam("text1") String t1, @RequestParam("text2") String t2,Model model){
        Double a,b,c;
        a=Double.parseDouble(t1) ;  //将t1转为double型变量,赋给a
        b=Double.parseDouble(t2);  //将t2转为double型变量,赋给b
        c=a*b;  //计算结果
        System.out.println(t1+"-"+t2);
        model.addAttribute("cValue",c);
        return "input.html";
    }
}
