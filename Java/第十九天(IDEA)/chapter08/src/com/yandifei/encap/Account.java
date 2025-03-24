package com.yandifei.encap;

public class Account {
    private String name;
    private double balance;
    private String password;

    public Account(String name, double balance, String password) {
        setName(name);
        setBalance(balance);
        setPassword(password);
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        if (password.length() < 6) {
            System.out.println("密码必须是6位，默认\"000000\"");
            this.password = "000000";
        } else {
            this.password = password;
        }
    }

    public Account() {
        this.password = "000000";
        this.name = "yan";
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if(name.length() >= 2 && name.length() <= 4) {
            System.out.println("姓名长度在位2-4位以内，默认为yan");
            this.name = "yan";
        } else {
            this.name = name;
        }
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        if(balance <= 20) {
            System.out.println("金额必须大于20，默认21元");
            this.balance = 21;
        } else {
            this.balance = balance;
        }
    }

    //获取信息
    public String getInfo(String password) {
        if (password.equals(this.password)) {
            return "姓名：" + this.name + " 余额" + this.balance + " 密码：" + this.password;
        } else {
            return "密码错误,无法获取信息";
        }
    }
}
