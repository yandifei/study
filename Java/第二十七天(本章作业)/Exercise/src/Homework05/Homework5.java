package Homework05;

public class Homework5 {
        public static void main(String[] args) {
            /*5.设计父类一员工类。
            子类：工人类(Worker)，农民类(Peasant)，教师类(Teacher),科学家类(Scientist),服务生类(Waiter)。
            （1）其中工人，农民，服务生只有基本工资
            （2）教师除基本工资外，还有课酬（元/天）
            （3）科学家除基本工资外，还有年终奖
            （4）编写一个测试类，将各种类型的员工的100%工资打印出来
             */
            Worker jack = new Worker("jack", 10000);
            jack.year_salary();
            Peasant smith = new Peasant("smith", 20000);
            smith.year_salary();
            Teacher teacher = new Teacher("顺平", 2000);
            teacher.year_salary();
            teacher.setClassDay(360);
            teacher.setClassSalary(1000);
            teacher.year_salary();

            //科学家
            Scientist scientist = new Scientist("钟南山",20000);
            scientist.setBonus(2000000);
            scientist.year_salary();

            Waiter waiter = new Waiter("小张", 2000);
            waiter.year_salary();
        }
}
