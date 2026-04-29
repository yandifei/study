package com.my.pojo;


import java.util.List;

public class Users {

  private int uid;
  private String uname;
  private int uage;
  // 新增关联的密码实体
  private Password passwordObj;

  // 一对多使用List
  private List<Order> orderList;

  public List<Order> getOrderList() {
    return orderList;
  }

  public void setOrderList(List<Order> orderList) {
    this.orderList = orderList;
  }

  public Password getPasswordObj() {
    return passwordObj;
  }

  public void setPasswordObj(Password passwordObj) {
    this.passwordObj = passwordObj;
  }

  public int getUid() {
    return uid;
  }

  public void setUid(int uid) {
    this.uid = uid;
  }


  public String getUname() {
    return uname;
  }

  public void setUname(String uname) {
    this.uname = uname;
  }


  public int getUage() {
    return uage;
  }

  public void setUage(int uage) {
    this.uage = uage;
  }

}
