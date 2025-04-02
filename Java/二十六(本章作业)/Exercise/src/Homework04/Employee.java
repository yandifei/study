package Homework04;

class Employee {
    private String name;
    private double one_day_salary;
    private int workdays;
    private double grade;

    public Employee(String name, double one_day_salary, int workdays, double grade) {
        this.name = name;
        this.one_day_salary = one_day_salary;
        this.workdays = workdays;
        this.grade = grade;
    }

    public double getGrade() {
        return grade;
    }

    public void setGrade(double grade) {
        this.grade = grade;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getOne_day_salary() {
        return one_day_salary;
    }

    public void setOne_day_salary(double one_day_salary) {
        this.one_day_salary = one_day_salary;
    }

    public int getWorkdays() {
        return workdays;
    }

    public void setWorkdays(int workdays) {
        this.workdays = workdays;
    }

    public void print_salary() {
        System.out.println("工资:" + one_day_salary * workdays);
    }
}