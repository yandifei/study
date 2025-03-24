import java.util.Scanner;

/**
 * 快捷键
 * ctrl + y      删除当前行
 * ctrl + d      复制当前行
 * alt + /       补全代码
 * ctrl + /      注释和取消注释
 * alt + enter  快速导入包的类
 * ctrl + alt + l 快速格式化代码(自动对齐、空格)
 * alt + insert   生成构造器
 * ctrl + shift + F10 运行代码
 * alt + h      查看父类
 * ctrl + b     查看方法(跳转到方法处)
 * ctrl + alt + v 自动生成对象名(代码写到一半后加.var也可以)
 */
public class IDEAStudy {
    //main就是一个模板的快捷键
    public static void main(String[] args) {
        Scanner myScanner = new Scanner(System.in);
        //sout是System.out.println();的模板，输入sout就可以自动补全很长的语句了
        System.out.println("模板");
        //fori是for的模板
        for (int i = 0; i < 1; i++) {
            System.out.println("设置->编辑器->实时模板(相当于命令库)");
        }
//        for(int i = 0; i < arr.length; i++) {
//            System.out.print(arr[i] + " ");
//        }
        Person person = new Person("yandifei", 10);


    }
}



class Person {
    String name;
    int age;
    //构造器-快捷键

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void print(String txt) {
        System.out.println(txt);
    }
}