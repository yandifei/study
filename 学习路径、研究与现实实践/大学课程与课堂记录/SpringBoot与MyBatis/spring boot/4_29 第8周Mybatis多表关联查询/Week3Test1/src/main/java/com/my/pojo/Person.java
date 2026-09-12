package com.my.pojo;


public class Person {

  private int id;
  private String name;
  private int age;
  private String sex;
  private int cardId;
  // 新增人员关联的证件
  private Idcard card;

  public Idcard getCard() {
    return card;
  }

  public void setCard(Idcard card) {
    this.card = card;
  }

  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
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


  public String getSex() {
    return sex;
  }

  public void setSex(String sex) {
    this.sex = sex;
  }


  public int getCardId() {
    return cardId;
  }

  public void setCardId(int cardId) {
    this.cardId = cardId;
  }

}
