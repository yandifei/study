package com.yandifei.poly.polyarr;

public class PloyArray {
    public static void main(String[] args) {
        Person[] person = new Person[5];
        person[0] = new Person(18,"person");
        person[1] = new Student(18,"student1",100);
        person[2] = new Student(19,"student2",99);
        person[3] = new Teacher(19,"teacher1",2000);
        person[4] = new Teacher(19,"teacher2",4000);
        for(int i = 0; i < person.length; i++) {
            System.out.println(person[i].say());
        }


    }
}
