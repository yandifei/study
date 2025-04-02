package Homework.Homework05;

public class Peasant extends Employee {
    public Peasant(String name, double salary) {
        super(name, salary);
    }

    @Override
    public void year_salary() {
        System.out.print("农民 ");
        super.year_salary();
    }
}
