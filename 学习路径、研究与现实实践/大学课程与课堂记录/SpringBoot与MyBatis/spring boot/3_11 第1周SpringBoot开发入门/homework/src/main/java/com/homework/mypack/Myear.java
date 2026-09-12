package com.homework.mypack;

public class Myear {
    public boolean isLeapYear(int year) {
        if (year % 4 == 0) {
            if (year % 100 == 0) {
                if (year % 400 == 0) {
                    return true;  // 能够被400整除，是闰年
                } else {
                    return false;  // 能够被100整除但不能被400整除，不是闰年
                }
            } else {
                return true;  // 能够被4整除但不能被100整除，是闰年
            }
        } else {
            return false;  // 不能够被4整除，不是闰年
        }
    }

}
