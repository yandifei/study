package yandifei.Exercise.Homework13;

public class Teacher extends Person{
    private double work_age;

    public Teacher(String name, char sex, int age, double work_age) {
        super(name, sex, age);
        this.work_age = work_age;
    }

    public double getWork_age() {
        return work_age;
    }

    public void setWork_age(double work_age) {
        this.work_age = work_age;
    }

    public String play() {
        return super.getName() + "爱玩象棋";
    }

    public void teacher() {
        System.out.println("我承诺，我会认真教学");
    }
}
