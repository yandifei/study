// 1. 数据：一个用户对象数组
const users = [
{ id: 1, name: "Alice", isActive: true },
{ id: 2, name: "Bob", isActive: false },
{ id: 3, name: "Charlie", isActive: true }
];
// 2. 目标：生成一个问候语列表，只包含活跃用户，并给每个人加上 "Mr." 前缀
// 3. 任务分解
const activeUsers = users.filter((user) => user.isActive === true); // .filter() 用于筛选
const greetings = activeUsers.map((user) => {
// 4. 解构获取 name
const { name } = user;
// 5. 箭头函数 + 字符串模板
return `Hello, Mr. ${name}!`;
});
// 6. 输出最终结果
console.log(greetings);
// 输出: ["Hello, Mr. Alice!", "Hello, Mr. Charlie!"]