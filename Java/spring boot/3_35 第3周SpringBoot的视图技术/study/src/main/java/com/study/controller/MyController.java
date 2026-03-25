package com.study.controller;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Date;
import java.util.Optional;

@Controller
public class MyController {

//    @GetMapping("/page1")
//    public String page1(){
//        return "aaa.html";
//    }

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

    @GetMapping("/page2")
    public String page2(Model model){
        int a = 27,  b = 28;
//      计算2个数值并传递给res来做后端传递数据给前端(单项数据绑定)
        model.addAttribute("res", a + b);
//      传递学号和姓名给前端
        model.addAttribute("studentId", "20235120801082");
        model.addAttribute("studentName", "潘炜德");
//        返回一bbb界面
        return "bbb.html";
    }

    @GetMapping("/input")
    public String input(){
        return "input.html";
    }

//    get方式获取前端数据
//    @GetMapping(value = "/getValue")  //这里对应上前端Form的action
//    public String getValue(HttpServletRequest request, Model model){
//        String t1,t2;
//        t1=request.getParameter("text1");//获取前端的name是text1控件的值
//        t2=request.getParameter("text2");//获取前端的name是text2控件的值
//        Double a,b,c;
//        a=Double.parseDouble(t1) ;  //将t1转为double型变量,赋给a
//        b=Double.parseDouble(t2);  //将t2转为double型变量,赋给b
//        c=a*b;  //计算结果
//        System.out.println(t1+"-"+t2);
//        model.addAttribute("cValue",c);  //将c的值放到model传给前端
//        return "input.html"; //返回input.html
//    }

    @PostMapping(value = "/getValue")  //这里对应上前端Form的action
    public String getValue(@RequestParam("text1") String t1, @RequestParam("text2") String t2, Model model){
        Double a,b,c;
        a=Double.parseDouble(t1) ;  //将t1转为double型变量,赋给a
        b=Double.parseDouble(t2);  //将t2转为double型变量,赋给b
        c=a*b;  //计算结果
        System.out.println(t1+"-"+t2);
        model.addAttribute("cValue",c);  //将c的值放到model传给前端
        return "input.html"; //返回input.html
    }

/*上机作业2：请编写一个判断体重胖瘦的练习：
国际上判断一个人体重胖瘦的方法，一般采用BMI法，即：
身体质量指数（BMI，Body  Mass  Index）=体重（公斤）除身高（米）的平方
在做胖瘦评估时，BMI小于18.5被称为营养不良，大于25被称为体重过重。中间的值为体重正常值.
例:  某人身高1.70 (米)，体重为52公斤.
则他的BMI值为 52/(1.70*1.70)=17.99
该值小于18.5,所以该同学体重偏瘦.
请编写一个网站,用户可以在控件中输入自己的身体和体重(注意单位是米和公斤), 点按钮后,显示出该用户的胖瘦情况.分别显示“偏瘦，标准，偏胖”
*/
//    定义根界面路由返回这个主页面（BMI计算）
    @GetMapping(value = "/")
    public String index(Model model){
        return "index.html";
    }

    @PostMapping(value = "/getBMI")
//  这里仅仅接受字符串，通过解析校验前端数据的合法性（前端校验不可靠）
    public String getBMI( @RequestParam("height") String heightStr,
                          @RequestParam("weight") String weightStr, Model model){
        // 检查是否为空或空白
        if(heightStr == null || heightStr.trim().isEmpty()) {
            model.addAttribute("res", "请输入身高");
            model.addAttribute( "errorType", "height");
            return "index.html";
        }
        if(weightStr == null || weightStr.trim().isEmpty()) {
            model.addAttribute("res", "请输入体重");
            model.addAttribute("errorType", "weight");
            return "index.html";
        }
//      加个异常捕获防止转换为double的时候就抛出异常导致前端无法响应和后端崩溃
        try {
            // 尝试将转换为double
            double height = Double.parseDouble(heightStr);
            double weight = Double.parseDouble(weightStr);

            // 计算BMI
            double bmi = weight / (height * height);

            // 判断身体状况
            String result;
            if(bmi < 18.5) {
                result = "偏瘦";
            } else if (bmi >= 18.5 && bmi < 25) {
                result = "正常";
            } else {
                result = "体重过重";
            }
            // 传递结果给前端
            model.addAttribute("res", result);
            model.addAttribute("bmiValue", String.format("%.2f", bmi));
            model.addAttribute("success", true);

        } catch (NumberFormatException e) {
            // 捕获非数字输入
            model.addAttribute("res", "请输入有效的身高和体重");
            model.addAttribute("errorType", "format");
        } catch (Exception e) {
            // 捕获其他未知的异常
            model.addAttribute("res", "系统错误，请稍后重试");
            model.addAttribute("errorType", "system");
        }

        return "index.html";
    }
}



