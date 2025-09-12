const numbers = [1, 2, 3, 4];
// .map 会遍历数组的每一项，并根据你提供的函数返回一个“新的”数组
const doubledNumbers = numbers.map((number) => {
return number * 2;
});
console.log("原数组:", numbers); // 输出: 原数组: [1, 2, 3, 4]
console.log("新数组 (翻倍后):", doubledNumbers); // 输出: 新数组 (翻倍后): [2, 4, 6, 8]
// 在 React 中，你会这样做：
const userNames = ["Alice", "Bob", "Charlie"];
// 假设这是 React 的 JSX 写法，现在我们用字符串模拟
const userListItems = userNames.map((name) => {
return `<li>${name}</li>`; // 把每个名字字符串，转换成一个 <li> 字符串
});
console.log(userListItems);
// 输出: ["<li>Alice</li>", "<li>Bob</li>", "<li>Charlie</li>"]
// 在 React 里，这些字符串就会被渲染成一个真正的列表！