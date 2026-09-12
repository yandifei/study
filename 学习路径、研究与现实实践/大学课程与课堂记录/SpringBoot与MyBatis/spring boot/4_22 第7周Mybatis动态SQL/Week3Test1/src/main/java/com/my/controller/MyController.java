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

//    注入StudentService去实现查询和增加操作
    @Autowired
    StudentService studentService;

    @GetMapping("/inputuser")//创建一个链接打开前端添加用户页
    public String inputuser(){
        return "inputuser.html";  //打开前端inputuser.html
    }

    @PostMapping("/adduser")  //获取前端传过来的值
    public String adduser(@RequestParam("name") String name,@RequestParam("age") String age,Model model){
        User user=new User();
//        user.setUname(name); //从前端给姓名赋值
//        user.setUage(Integer.parseInt(age));//从前端给年龄赋值,注意转换为整型
//        int count=userService.addUser(user); //调用service方法添加数据
//        if(count==0)  //如果返回0就失败
//            model.addAttribute("result","添加失败"); //向前端传递失败
//        else
//            model.addAttribute("result","添加成功");//向前端传递成功
//        return "adduserresult.html"; //打开adduserresult.html输出成功与否

//        动态sql实现的用户增加逻辑
        if (name != null && !name.isEmpty()) {
            user.setUname(name);
        }
        if (age != null && !age.isEmpty()) {
            user.setUage(Integer.parseInt(age));
        }
        int count = userService.addUser(user);
        if (count > 0) {
            model.addAttribute("result", "添加成功");
        } else {
            model.addAttribute("result", "添加失败");
        }
        return "adduserresult.html";
    }

    @GetMapping("/finduser")  //创建一个链接打开前端查询页
    public String finduser(Model model){
        List<User> userList=userService.findAllUser(); //调用uservice读取值
        model.addAttribute("userList",userList); //将对象传给前端
        return "finduser.html";
    }

    @PostMapping("/getuser")
    public String getValue(@RequestParam(value="uid",required=false) String uid,
                           @RequestParam(value="uname",required=false) String uname,
                           @RequestParam(value="uage",required=false) String uage,
                           Model model){
        User user =new User();
        if(uid!="")  //如果不为空就赋值
            user.setUid(Integer.parseInt(uid));
        if(uname!="")
            user.setUname(uname);
        if(uage!="")
            user.setUage(Integer.parseInt(uage));
        List<User> userList=userService.findUser(user); //从数据库读取值
        model.addAttribute("userList",userList);//将对象传给前端
        model.addAttribute("uid",uid);//将值传给前端
        model.addAttribute("uname",uname);
        model.addAttribute("uage",uage);
        return "finduser.html";
    }


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

    // 显示添加学生页面
    @GetMapping("/addstudent")
    public String showAddStudentPage() {
        return "addstudent";
    }

    // 处理添加学生请求（动态SQL）
    @PostMapping("/addstudent")
    public String addStudent(@RequestParam(value = "sname", required = false) String sname,
                             @RequestParam(value = "sage", required = false) String sage,
                             Model model) {
        Student student = new Student();
        if (sname != null && !sname.isEmpty()) {
            student.setSname(sname);
        }
        if (sage != null && !sage.isEmpty()) {
            try {
                student.setSage(Integer.parseInt(sage));
            } catch (NumberFormatException e) {
                model.addAttribute("result", "年龄必须为数字！");
                return "addstudentresult";
            }
        }
        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            model.addAttribute("result", "添加学生成功！");
        } else {
            model.addAttribute("result", "添加失败，请检查数据。");
        }
        return "addstudentresult";
    }
}
