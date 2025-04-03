package Homework05;

public class Waiter extends Employee {
    public Waiter(String name, double salary) {
        super(name, salary);
    }

    @Override
    public void year_salary() {
        System.out.print("服务员 ");
        super.year_salary();
    }
}
