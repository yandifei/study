1. switch表达式的类型要和case后面的**类型一致** ，或者是可以**自动转换**成可以相互比较的类型，比如输入的是字符，而常量是int
2. switch(表达式)，表达式的返回值必须是(byte,short,int,char,enum,String)这里面的类型，不能是**float、double、long**，即为switch和case的类型不能是浮点型长整型
3. case子句中的值必须是常量(1，a')或常量表达式,而不能是变量
```java
char c1 = 'a';
char c2 = 'c';
switch(c) {
    case 'a' :
        System.out.println("星期一");
    case c2 : //这种写法是错误的，c2是常量
        System.out.println("星期二");
    case 'c' + 1 : //这个是可以的
        System.out.println("星期三");
}
```
4. default是可以省略的，省略的话就是其他结果都不做任何处理，程序直接跳到switch语句块
5. break语句用来在执行完一个case分支后使程序跳出switch语句块。没有break就会直接穿透（真实穿透伤害），因为如果没有break，就会执行下一个case里面的程序不管有没有满足case里面的条件。遇到break后就会立刻退出当前的选择分支
### switch 和 if 什么什么时候选择最好
如果判断的具体数值不多，
而且符合byte、 short 、int、char, enum[枚举]String这6种类型。虽然两个语句都可以使用，建议使用swtich语句。