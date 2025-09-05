// 用 let 声明一个可能会改变的变量
let score = 10;
console.log("初始分数:", score); // 输出: 初始分数: 10
score = 15;
console.log("更新后分数:", score); // 输出: 更新后分数: 15
// 用 const 声明一个常量 (不会改变的值)
// 在 React 中，我们优先使用 const，除非我们知道这个变量需要被重新赋值。
const name = "张三";
console.log("姓名:", name); // 输出: 姓名: 张三
// 尝试修改 const 声明的变量会报错，这能帮助我们避免意外修改数据
// name = "李四"; // 取消这行注释会看到错误