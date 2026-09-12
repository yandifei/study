下面是按你**当前代码真实语义**改过的“设计原则”（把冲突点都对齐了）。我尽量保持原来 8 条结构，只改必要内容。

## 设计原则（与当前代码一致版）

1. **单例 Factory、可重启 Playwright 会话**：同一时刻只允许存在一个活跃的 `PlaywrightFactory` 实例（并发安全）；调用 `close()` 后会释放单例（`_instance=None`），允许在同一进程内重新创建 Factory 并再次执行 `sync_playwright().start()`。

2. **显式关闭优先**：提供 `close()` 作为统一的幂等回收入口；业务代码应显式调用 `close()`（必要时可封装 `with` 管理，但当前实现未内置 `with`）。

3. **退出兜底**：在 Factory 初始化时注册 `atexit.register(self.close)`，在解释器正常退出时自动触发 `close()` 做兜底回收（不依赖 `__del__`）。

4. **Browser 复用由调用方决定，Factory 保留多策略扩展能力**：Factory 提供 `new_browser()` 创建并登记多个 Browser；同时提供 `get_browser_()` 返回已登记 Browser 的副本列表，调用方可自行选择复用哪一个 Browser。后续可扩展“默认复用单 Browser / 按 launch 策略复用”的策略方法，但当前默认不自动复用。

5. **所有权（ownership）严格**：Factory 仅管理并回收由自己创建并登记的 Browser/Context。`new_context(browser=...)` 要求传入的 browser 必须来自本 Factory（已登记），否则抛出异常；不支持对外部 browser/context 的隐式接管（后续若需要可新增显式 `adopt_*` 接口）。

6. **回收顺序固定且 stop 至多一次**：统一回收顺序为 `Contexts → Browsers → Playwright`。通过 `_playwright_flag` 保证 `close()` 幂等：一旦关闭完成，后续再调用 `close()` 不会重复 stop。

7. **注册表线程安全，关闭在锁外执行**：所有创建/登记/移除（Browser/Context registry）操作均在同一把可重入锁保护下完成；`close()` 在锁内完成“置状态 + 拷贝 + 清空 registry”，随后在锁外执行实际 `close()`/`stop()`，避免阻塞其他线程。

8. **Page 不纳入生命周期管理**：Factory 仅提供 `new_page(context)` 的便捷创建，不追踪 Page；Page 的回收依赖 `context.close()` 的级联行为，如需 Page 级别的特殊回收策略由上层业务实现。

---

如果你后面准备加 `with`（`managed_context()`）或“默认复用 browser（get_or_create_browser）”，我也可以顺手帮你把原则再升级一版，让文档和代码继续保持一致。
