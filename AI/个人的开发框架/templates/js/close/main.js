// 主题切换
function toggleTheme() {
  const current = document.documentElement.dataset.theme;
  document.documentElement.dataset.theme = current === "dark" ? "light" : "dark";
}

// 绑定按钮事件
document.getElementById("themeBtn").addEventListener("click", toggleTheme);

// 关闭窗口的函数
setTimeout(() => {
  // 更新 UI 提示
  const title = document.querySelector(".card h2");
  const desc = document.querySelector(".card p");
  if (title) title.textContent = "操作已完成";
  if (desc) desc.innerHTML = "请手动关闭此标签页～<br>拜拜！✨";
  window.close();
}, 3000);

// 发起请求，并在成功后触发关闭
fetch(window.location.href, {
  method: 'DELETE'
})