package com.my.pojo;


import java.util.List;

public class TStudent {

  private int sid;
  private String sname;
  private int sage;
  private List<Score> scoreList;

  public List<Score> getScoreList() {
    return scoreList;
  }

  public void setScoreList(List<Score> scoreList) {
    this.scoreList = scoreList;
  }



  public int getSid() {
    return sid;
  }

  public void setSid(int sid) {
    this.sid = sid;
  }


  public String getSname() {
    return sname;
  }

  public void setSname(String sname) {
    this.sname = sname;
  }


  public int getSage() {
    return sage;
  }

  public void setSage(int sage) {
    this.sage = sage;
  }

}
