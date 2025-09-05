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