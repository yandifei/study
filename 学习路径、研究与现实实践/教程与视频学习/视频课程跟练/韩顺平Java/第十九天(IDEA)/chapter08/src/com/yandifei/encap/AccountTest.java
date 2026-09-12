package com.yandifei.encap;
/*创建程序，在其中定义两个类：Account和AccountTest类体会Java的封装性。
1.Account类要求具有属性：姓名（长度为2位3位或4位）、余额（必须>20)、
密码（必须是六位），如果不满足，则给出提示信息，并给默认值（程序员自己定)
2.通过setXxx的方法给Account的属性赋值。
3.在AccountTest中测试*/
public class AccountTest {
    public static void main(String[] args) {
        Account account = new Account();
        System.out.println(account.getInfo("000000"));
        Account account1 = new Account("yan",1100,"123456");
        System.out.println(account1.getInfo("123456"));

    }
}

