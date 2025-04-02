package Homework.Homework05;

public class Teacher extends Employee {
    private int classDay;
    private double classSalary;

    public Teacher(String name, double salary) {
        super(name, salary);
    }

    public int getClassDay() {
        return classDay;
    }

    public void setClassDay(int classDay) {
        this.classDay = classDay;
    }

    public double getClassSalary() {
        return classSalary;
    }

    public void setClassSalary(double classSalary) {
        this.classSalary = classSalary;
    }

    @Override
    public void year_salary() {
        System.out.println("教师 " + getName() +"全年的工资是:" + (getSalary() * 12 + classDay * classSalary));
    }
}
