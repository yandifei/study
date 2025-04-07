package yandifei.Exercise.Homework11;

public class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void run() {
        System.out.println("person run");
    }

    public void eat() {
        System.out.println("person eat");
    }
}
