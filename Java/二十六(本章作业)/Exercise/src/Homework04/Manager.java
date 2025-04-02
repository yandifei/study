package Homework04;

public class Manager extends Employee {
    private double bonus;

    public Manager(String name, double one_day_salary, int workdays, double grade) {
        super(name, one_day_salary, workdays, grade);
    }

    public double getBonus() {
        return bonus;
    }

    public void setBonus(double bonus) {
        this.bonus = bonus;
    }

    @Override
    public void print_salary() {
        System.out.println("经理" + getName()+ "工资是="+ bonus + getOne_day_salary() * getWorkdays()* getBonus());
    }
}
