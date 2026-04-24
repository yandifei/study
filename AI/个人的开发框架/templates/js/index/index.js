// 版本获取
document.addEventListener("DOMContentLoaded", async () => {
  try {
    // 发起 POST 请求到后端
    const response = await fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });
    if (response.ok) {
        // 定位元素并修改文本内容，后端返回的数据格式是 {"version": "3.1.2"}
        const data = await response.json(); // 先解析
        const versionText = data.version || "未知版本"; // 防止后端没传 version
        document.getElementById("version-text").textContent = versionText;
    }
  } catch (error) {
    console.error("版本号获取失败:", error);
  }
});

// 主题切换 + 图标切换
function toggleTheme() {
  const html = document.documentElement;
  const current = html.dataset.theme;
  const newTheme = current === "dark" ? "light" : "dark";
  html.dataset.theme = newTheme;

  // 更新图标
  const icon = document.getElementById("themeIcon");
  if (icon) {
    icon.textContent = newTheme === "dark" ? "🌙" : "☀️";
  }
}

// 绑定主题按钮
document.getElementById("themeBtn")?.addEventListener("click", toggleTheme);

// 修改任务按钮点击反馈
document.querySelectorAll(".task-btn").forEach(link => {
  link.addEventListener("click", function (e) {
    // 检查：如果是跳转到状态页的监控按钮，不拦截，让它正常跳转
    if (this.classList.contains('monitor-btn')) {
      return;
    }

    e.preventDefault(); // 仅拦截真正的任务启动按钮

    const original = this.textContent.trim();
    this.textContent = "启动中...";
    this.style.opacity = "0.6";
    this.style.pointerEvents = "none";

    fetch(this.href)
      .then(r => {
        this.textContent = original + (r.ok ? " ✓" : " ✗");
        setTimeout(() => {
          this.textContent = original;
          this.style.opacity = "1";
          this.style.pointerEvents = "auto";
        }, r.ok ? 1800 : 3500);
      })
      .catch(() => {
        this.textContent = original + " ✗";
        setTimeout(() => {
          this.textContent = original;
          this.style.opacity = "1";
          this.style.pointerEvents = "auto";
        }, 3500);
      });
  });
});

// 新增：关闭程序按钮处理
const shutdownBtn = document.getElementById("shutdownBtn");
if (shutdownBtn) {
  shutdownBtn.addEventListener("click", function (e) {
    // 当前窗口
    window.open("/close", "_self");
  });
}