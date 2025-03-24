package com.package_study.pack;

import com.package_study.modifier.A;

public class Test {
    public static void main(String[] args) {
        A a = new A();
        //在不同包下，可以访问public 修饰的属性或方法
        //但是不能访问 protected、默认、private修饰
//        System.out.println(a.n1 + a.n4);
    }
}
