package com.study.entity;

/**
 * 用户实体类
 */
public class Users {
    private Integer uid;      // 用户ID
    private String uname;     // 用户名
    private Integer uage;     // 用户年龄

    public Users() {
    }

    public Users(Integer uid, String uname, Integer uage) {
        this.uid = uid;
        this.uname = uname;
        this.uage = uage;
    }

    public Integer getUid() {
        return uid;
    }

    public void setUid(Integer uid) {
        this.uid = uid;
    }

    public String getUname() {
        return uname;
    }

    public void setUname(String uname) {
        this.uname = uname;
    }

    public Integer getUage() {
        return uage;
    }

    public void setUage(Integer uage) {
        this.uage = uage;
    }

    @Override
    public String toString() {
        return "Users{" +
                "uid=" + uid +
                ", uname='" + uname + '\'' +
                ", uage=" + uage +
                '}';
    }
}
