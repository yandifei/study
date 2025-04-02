package Homework02;

public class Homework2 {
    //写出四种访问修饰符和各自的访问权限
    //公共的修饰符，所有类所有包都可以使用
    public void a() {}
    //受保护的类，不同的目录不能使用，只能在同一个目录下使用这个类
    protected void b() {};
    //默认的修饰符，只能在这个包里面调用
    void c() {};
    //隐私修饰符，只能被这个类所访问
    private void d() {};
}
