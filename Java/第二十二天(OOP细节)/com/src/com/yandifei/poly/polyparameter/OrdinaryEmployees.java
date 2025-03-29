package com.yandifei.poly.polyparameter;

public class OrdinaryEmployees extends Employee{
    private double salary;

    public OrdinaryEmployees(String name, double salary) {
        super(name, salary);
        this.salary = salary;
    }

    @Override
    public double getSalary() {
        return salary;
    }

    @Override
    public void setSalary(double salary) {
        this.salary = salary;
    }

    //重写普通员工年薪的方法
    public String getAnnual()  {
        return "普通员工的年薪:" + (this.salary * 12);
    }

    public String work() {
        return "开始普通员工的工作";
    }

}
