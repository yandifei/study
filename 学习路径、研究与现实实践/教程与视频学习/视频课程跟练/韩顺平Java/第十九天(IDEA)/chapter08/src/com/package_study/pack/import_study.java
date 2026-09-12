package com.package_study.pack;

import java.util.Arrays;

//建议：我们需要使用到哪个类，就导入哪个类即可，不建议使用*导入
//import java.util.Scanner;   //表示只会引入java.util 包下的Scanner
//import java.util.*;  //表示将java.util包下的所有类都引入（导入）
public class import_study {
    public static void main(String[] args) {
        //案例：使用系统提供Arrays完成数组排序
        int[] arr = {-1, 20, 13, 3};
        //对他进行排序
        //传统方法是自己编写代码（冒泡排序）
        //系统是提供了相关的类，可以方便完成 Arrays
        Arrays.sort(arr);
        for(int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
    }
}
