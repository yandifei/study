package com.yandifei.poly.polyparameter;

public class Manager extends Employee {
    private double salary;
    private double bonus;

    public Manager(String name, double salary, double bonus) {
        super(name,salary);
        this.salary = salary;
        this.bonus = bonus;
    }

    @Override
    public double getSalary() {
        return salary;
    }

    @Override
    public void setSalary(double salary) {
        this.salary = salary;
    }

    public double getBonus() {
        return bonus;
    }

    public void setBonus(double bonus) {
        this.bonus = bonus;
    }

    //重写经理年薪的方法
    public String getAnnual()  {
        return "经理的年薪:" + (this.salary * 12);
    }

    public String manage() {
        return "开始经理的管理工作";
    }
}
