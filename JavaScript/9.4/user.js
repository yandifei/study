// 导出一个默认的函数
export default function getUser() {
return { name: "张三", id: 101 };
}
// 注意：同一个文件可以同时有命名导出和默认导出
export const userRole = "admin";
