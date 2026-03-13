package com.sang;
import com.sang.mypack.Myear;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
        Myear myear=new Myear();
        System.out.println(myear.isLeapYear(2026));

    }
}
