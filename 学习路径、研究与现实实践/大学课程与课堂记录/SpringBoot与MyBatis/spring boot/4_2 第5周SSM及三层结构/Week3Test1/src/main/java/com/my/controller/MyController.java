package com.my.controller;

import com.my.domain.Student;
import com.my.domain.User;
import com.my.service.StudentService;
import com.my.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Conditional;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpServletRequest;
import java.util.Date;
import java.util.List;


@Controller
public class MyController {
    @Autowired
    UserService userService;

    @GetMapping("/finduser")  //创建一个链接打开前端查询页
    public String finduser(Model model){
        List<User> userList=userService.findAllUser(); //调用uservice读取值
        model.addAttribute("userList",userList); //将对象传给前端
        return "finduser.html";
    }

    @PostMapping(value = "/getuser")  //这个链接接收前传过来的值
    public String getValue(@RequestParam("text1") String name,Model model){
        List<User> userList=userService.findUserByName(name); //调用uservice读取值
        model.addAttribute("userList",userList); //将对象传给前端
        model.addAttribute("username",name); //将用户查询的名字传回去
        return "finduser.html";
    }

    @Autowired
    StudentService studentService;   // 注入 StudentService

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

    // 显示所有学生,首次加载页面
    @GetMapping("/studentList")
    public String showAllStudents(Model model) {
        List<Student> students = studentService.findAllStudent();
        model.addAttribute("studentList", students);
        return "studentList.html";
    }

    // 处理按姓名查询的请求
    @PostMapping("/searchStudent")
    public String searchStudent(@RequestParam("sname") String sname, Model model) {
        List<Student> students = studentService.findStudentByName(sname);
        model.addAttribute("studentList", students);
        model.addAttribute("sname", sname);   // 回显输入框的值
        return "studentList.html";
    }
}
