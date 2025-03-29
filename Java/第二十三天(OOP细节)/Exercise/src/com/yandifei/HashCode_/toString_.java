package com.yandifei.HashCode_;

public class toString_ {
    public static void main(String[] args) {
        /*Object 的toString源码
        public String toString() {
            return this.getClass().getName() + "@" + Integer.toHexString(this.hashCode());
         }

         源码分析
        (1)getClass().getName() //类的全类名(包名+类名)
        (2)Integer.toHexString(this.hashCode()) //将对象的hashCode值转为16进制
         */
        Monster monster = new Monster("小妖怪","巡山的",1000);
        System.out.println(monster.toString()); //哈希值转为16进制
        System.out.println(monster.hashCode()); //十进制的哈希值
        System.out.println("=======================");
        System.out.println(monster);    //如果什么都不写，默认调用monster.toString()


    }
}

class Monster { //妖怪
    private String name;
    private String job;
    private double sal;

    public Monster(String name, String job, double sal) {
        this.name = name;
        this.job = job;
        this.sal = sal;
    }

    //重写toString方法，输出对象的属性
    //使用快捷键可生成alt + insert -> toString

    @Override
    public String toString() {  //重写后一般都是把对象的属性值输出，当然程序员也可以自己定制
        return "Monster{" +
                "name='" + name + '\'' +
                ", job='" + job + '\'' +
                ", sal=" + sal +
                '}';
    }
}