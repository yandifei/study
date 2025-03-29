package com.yandifei.poly.polyparameter;

public class Test {
    public static void main(String[] args) {
        Test test = new Test();
//        Employee e = new Employee("抽象员工", 1000);

        Employee e = new OrdinaryEmployees("普通员工", 3000);
        System.out.println(test.showEmpAnnual(e));
        System.out.println(test.testWork(e));


        e = new Manager("经理",10000,3000);
        System.out.println(test.showEmpAnnual(e));
        System.out.println(test.testWork(e));

    }
    public String showEmpAnnual(Employee e) {
       return e.getAnnual();
    }

    public String testWork(Employee e) {
        if(e instanceof OrdinaryEmployees) {
            return ((OrdinaryEmployees)e).work();
        }
        return ((Manager)e).manage();
    }
}
