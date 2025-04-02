package Homework04;

public class Worker extends Employee {
    public Worker(String name, double one_day_salary, int workdays, double grade) {
        super(name, one_day_salary, workdays, grade);
    }

    @Override
    public void print_salary() {
        System.out.print("普通员工 ");
        super.print_salary();
    }
}
