package com.yandifei.debug_;


import java.util.Arrays;

public class Debug {
    public static void main(String[] args) {
        /*调试(debug)学学习
        F7(跳入)F8(跳过)shift+F8(跳出)F9(resume,执行到下一个断点)
        F7:跳入方法内
        F8:逐行执行代码
        shift+F8:跳出方法
        alt + shift + F7强制进入
         */
        //debug 数组
//        int sum = 0;
//        for (int i= 0; i < 5; i++) {
//            sum += i;
//            System.out.println(" i = " + i);
//            System.out.println(" sum = " + sum);
//        }
//        System.out.println("退出for....");
//        int[] arr = {1,50,99,100,5,10,9};
//        Arrays.sort(arr);
//        for(int i = 0; i < arr.length; i++) {
//            System.out.print(arr[i] + " ");
//        }
//        System.out.println("1");
        int a = 1, b = 1;
        Debug p = new Debug();
        p.count(a);
        System.out.println(a);
    }

    public int count(int a) {
        a += a;
        return a;
    }
}
