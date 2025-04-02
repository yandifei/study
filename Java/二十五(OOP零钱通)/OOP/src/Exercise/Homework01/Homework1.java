package Exercise.Homework01;

public class Homework1 {
    //定义一个Person类{name,age,job},初始化Person 对象数组，有3个person对象，并
    // 按照age从大到小进行排序，提示，使用冒泡排序Homework01java
    public static void main(String[] args) {
        Person[] person = new Person[3];
        person[0] = new Person("jack", 10, "JavaEE工程师");
        person[1] = new Person("tom", 50, "大数据工程师");
        person[2] = new Person("marry", 30, "PHP工程师");

        for (int i = 0; i < person.length; i++) {
            System.out.println(person[i].getName() + ":" + person[i].getAge() + "岁");
        }
        Person temp; //临时变量用来交换
        for (int i = 0; i < person.length; i++) {
            for (int j = 0; j < person.length - i -1; j++) {
                if (person[j].getAge() > person[j + 1].getAge()) {
                    temp = person[j + 1];
                    person[j + 1] = person[j];
                    person[j] = temp;
                }
            }
        }

        System.out.println("排序后");
        for (int i = 0; i < person.length; i++) {
            System.out.println(person[i].getName() + ":" + person[i].getAge() + "岁");
        }
    }
}
