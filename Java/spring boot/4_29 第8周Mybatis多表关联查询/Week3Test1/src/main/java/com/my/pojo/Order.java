package com.my.pojo;


public class Order {

  private int id;
  private String productname;
  private double price;
  private int number;
  private int userid;


  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
  }


  public String getProductname() {
    return productname;
  }

  public void setProductname(String productname) {
    this.productname = productname;
  }


  public double getPrice() {
    return price;
  }

  public void setPrice(double price) {
    this.price = price;
  }


  public int getNumber() {
    return number;
  }

  public void setNumber(int number) {
    this.number = number;
  }


  public int getUserid() {
    return userid;
  }

  public void setUserid(int userid) {
    this.userid = userid;
  }

}
