// 传统函数
function sayHello(name) {
return `你好, ${name}!`;
}
console.log(sayHello("传统函数"));
// 箭头函数 (Arrow Function) - React 中最常用的写法，更简洁！
const sayHelloArrow = (name) => {
return `你好, ${name}!`;
};
console.log(sayHelloArrow("箭头函数"));
// 如果函数体只有一行返回语句，可以更简洁：
const add = (a, b) => a + b;
console.log("2 + 3 =", add(2, 3)); // 输出: 2 + 3 = 5
// 在 React 中，你会这样写一个点击事件处理函数：
const handleClick = () => {
console.log("按钮被点击了！");
};
handleClick();
