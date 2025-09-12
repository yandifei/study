const user = {
name: "David",
age: 30,
email: "david@example.com"
};
// 传统方式获取值
// const name = user.name;
// const age = user.age;
// 使用解构，一行搞定！
const { name, age } = user;
console.log(`姓名: ${name}, 年龄: ${age}`); // 输出: 姓名: David, 年龄: 30
// --- 展开语法 (...) ---
// 1. 用于复制对象/数组 (React 中更新 state 的核心技巧)
const numbers = [1, 2, 3];
const newNumbers = [...numbers, 4, 5]; // 复制 numbers，并在后面加上 4, 5
console.log(newNumbers); // 输出: [1, 2, 3, 4, 5]
// 2. 更新对象的属性
const updatedUser = {
...user, // 复制 user 对象的所有属性
age: 31 // 然后用新的 age 覆盖旧的
};
console.log(updatedUser); // 输出: {name: "David", age: 31, email: "david@example.com"}