const isLoggedIn = false;
// 传统 if/else
let message;
if (isLoggedIn) {
message = "欢迎回来！";
} else {
message = "请先登录。";
}
console.log(message); // 输出: 请先登录。
// 使用三元运算符: condition ? value_if_true : value_if_false
const ternaryMessage = isLoggedIn ? "欢迎回来！" : "请先登录。";
console.log(ternaryMessage); // 输出: 请先登录。
// 在 React 中会这样用：
// { isLoggedIn ? <UserProfile /> : <LoginForm /> }
