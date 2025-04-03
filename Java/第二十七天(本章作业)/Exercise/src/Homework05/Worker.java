package Homework05;

public class Worker extends Employee {
    public Worker(String name, double salary) {
        super(name, salary);
    }

    @Override
    public void year_salary() {
        System.out.print("工人 ");
        super.year_salary();
    }
}
