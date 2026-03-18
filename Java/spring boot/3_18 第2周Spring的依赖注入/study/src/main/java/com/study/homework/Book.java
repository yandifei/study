package com.study.homework;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Book {
    @Value("软件工程")
    private String Bookname;  //书名
    @Value("广东培正学院")
    private String publis; //出版社
    @Value("10000000000")
    private double price;//价格
    @Autowired
    private Author author;

    public String getBookname() {
        return Bookname;
    }

    public void setBookname(String bookname) {
        Bookname = bookname;
    }

    public String getPublis() {
        return publis;
    }

    public void setPublis(String publis) {
        this.publis = publis;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public Author getAuthor() {
        return author;
    }

    public void setAuthor(Author author) {
        this.author = author;
    }

    @Override
    public String toString() {
        return "Book{" +
                "Bookname='" + Bookname + '\'' +
                ", publis='" + publis + '\'' +
                ", price=" + price +
                ", author=" + author +
                '}';
    }
}
