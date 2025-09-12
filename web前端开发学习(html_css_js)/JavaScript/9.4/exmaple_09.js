// for 循环
for (let i = 0; i < 5; i++) {
console.log("数字是 " + i);
}
// for...of 循环:
// 用于遍历可迭代对象，例如数组、字符串等。它直接访问每个元素的值，而不是索引
const arr = [1, 2, 3, 4, 5];
for (const num of arr) {
console.log(num);
}
const colors = ["red", "green", "blue"];
for (const color of colors) {
console.log(color);
}
// for...in 循环:
// 用于遍历对象的属性，而不是遍历对象中的值。它返回对象的键（属性名）。
const person = {
name: "张三",
age: 30,
city: "北京"
};
for (const key in person) {
console.log(key + ": " + person[key]);
}
// while 循环:
// 循环条件为 true 时执行代码块。
let i = 0;
while (i < 5) {
console.log("数字是 " + i);
i++;
}
// do...while 循环:
// 和 while 循环类似，但 ensure 循环至少会执行一次。
let j = 0;
do {
console.log("数字是 " + j);
j++;
} while (j < 5);

class Student extends Person {
// 子类的构造函数
constructor(name, age, studentId) {
// 必须先调用 super() 来初始化父类的属性
super(name, age);
// 然后再初始化子类特有的属性
this.studentId = studentId;
}
// 子类可以拥有自己的新方法
study() {
console.log(`${this.name} 正在努力学习...`);
}
// 子类可以重写（Override）父类的方法
sayHello() {
// 调用父类的 sayHello 方法，并增加自己的逻辑
super.sayHello();
console.log(`我的学号是 ${this.studentId}。`);
}
}
// 创建一个 Student 类的实例
const student1 = new Student('王五', 20, '2023001');
// 调用子类的方法
student1.sayHello();
/* 输出:
大家好，我叫 王五，今年 20 岁。
我的学号是 2023001。
*/
student1.study(); // 输出: 王五 正在努力学习...
// 继承了父类的方法
console.log(student1.getAge()); // 输出: 20