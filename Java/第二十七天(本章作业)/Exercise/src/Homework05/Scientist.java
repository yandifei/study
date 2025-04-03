package Homework05;

public class Scientist extends Employee {
    private double bonus;

    public Scientist(String name, double salary) {
        super(name, salary);
    }

    public double getBonus() {
        return bonus;
    }

    public void setBonus(double bonus) {
        this.bonus = bonus;
    }

    @Override
    public void year_salary() {
        System.out.println("科学家 " + getName() + "全年的工资是:" + (getSalary() * 12 + bonus));
    }
}
