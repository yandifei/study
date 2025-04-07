package yandifei.Exercise.Homework10;

public class Doctor {
    String name;
    int age;
    String job;
    char gender;
    double sal;

    public Doctor(String name, int age, String job, char gender, double sal) {
        this.name = name;
        this.age = age;
        this.job = job;
        this.gender = gender;
        this.sal = sal;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getJob() {
        return job;
    }

    public void setJob(String job) {
        this.job = job;
    }

    public char getGender() {
        return gender;
    }

    public void setGender(char gender) {
        this.gender = gender;
    }

    public double getSal() {
        return sal;
    }

    public void setSal(double sal) {
        this.sal = sal;
    }

    public boolean equals(Object obj) {
        //判断2个对象是否相同
        if (this == obj) {
            return true;
        }

        //判断obj 是否是 Doctor的类型和子类
        //过关斩将 校验方式
        if (!(obj instanceof Doctor)) { //不是同一个对象，无法比较
            return false;
        }

        //向下转型，因为obj的运行类型是Doctor或其子类型
        Doctor doctor = (Doctor)obj;
        return this.name.equals(doctor.name) && this.age == doctor.age
                && this.job.equals(doctor.job) && this.gender == doctor.gender
                && this.sal == doctor.sal;
    }
}
