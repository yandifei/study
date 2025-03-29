package com.yandifei.Finalize_;

public class Finalize_ {
    public static void main(String[] args) {
        //java9中明确标记废弃，直到现在的java23都还没有完全移除
        Car bmw = new Car("宝马");
        //滞空，无法引用变成垃圾自动回收
        //这时car对象就是一个垃圾，垃圾回收器会回收（销毁）对象，在销毁对象前，会调用该对象finalize方法
        //程序员就可以在finalize，写自己的业务逻辑代码(比如释放资源，数据库连接，或者时打开的文件)
        bmw = null;
        //如果不重写，默认调用Object的finalize方法，即默认处理
        //如果程序员重写了finalize，就可以实现自己的逻辑

        System.out.println("==========对象滞空了==========");
        //不是变成垃圾了就立刻调用finalize回收，如果一变成垃圾就回收意味着finalize得实时监控，效率极低
        //垃圾回收机制的调用是由系统决定的，即CG算法，也可以通过System.gc()主动触发垃圾回收机制
        //但是调用System.gc()后不是100%立即运行垃圾回收器(大概率立即运行)
        System.gc();
        System.out.println("调用垃圾回收器");
        //在实际开发中，几乎不会运用finalize，所以更多就是为了应付面试

    }
}

class Car {
    private String name;
    //属性、资源、连接、文件打开，如果不自己回收，系统会自动回收，但是自己回收效果会更好
    public Car(String name) {
        this.name = name;
    }

    //重写finalize方法
    //快捷键生成alt + insert
    @Override
    protected void finalize() throws Throwable {
//        super.finalize();
        System.out.println("我们销毁 汽车" + this.name);
        System.out.println("释放了某些资源...");
    }
}