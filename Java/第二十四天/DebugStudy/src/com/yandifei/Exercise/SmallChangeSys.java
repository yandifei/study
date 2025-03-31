package com.yandifei.Exercise;

import java.util.Scanner;

public class SmallChangeSys {
    //化繁为简
    //1。先完成显示菜单，并可以选择菜单，给出对应提示
    //2.完成零钱通明细
    public static void main(String[] args) {
        //定义相关的变量
        boolean loop = true;    //是否还要循环
        Scanner scanner = new Scanner(System.in);
        String key = "";//接收键盘的字符串

        //2.零钱通明细
        //（1）可以把收益入账和消费，保存到数组（2）可以使用对象（3）简单的话可以使用String拼接
        String details = "--------------零钱通菜单--------------";

        do {
            System.out.println("\n==============零钱通菜单==============");
            System.out.println("\t\t\t1 零钱通明细");
            System.out.println("\t\t\t2 收益入账");
            System.out.println("\t\t\t3 消费");
            System.out.println("\t\t\t4 退\t出");
            System.out.print("请选择(1-4):");

            key = scanner.next();//接收键盘字符
            //使用switch分支控制
            switch (key) {
                case "1" :
                    System.out.println("1 零钱通明细");
                    System.out.println(details);
                    break;
                case "2" :
                    System.out.println("2 收益入账");
                    break;
                case "3" :
                    System.out.println("3 消费");
                    break;
                case "4" :
                    System.out.println("4 退\t出");
                    loop = false;//设置退出标志
                    break;
                default:
                    System.out.println("选择有误，请重新选择");
            }
        }while (loop);
        System.out.println("===========退出了零钱通项目===========");
//        SmallChangeSys smallChangeSys = new SmallChangeSys();
    }
}
