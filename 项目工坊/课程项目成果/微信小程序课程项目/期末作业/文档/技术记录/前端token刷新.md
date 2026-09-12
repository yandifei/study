# 微信小程序 Token 自动刷新 —— 请求拦截器

## 一、问题背景

后端使用 JWT 双 token 机制：

| Token | 生命周期 | 用途 |
|---|---|---|
| `access_token` | 短（如 30 分钟） | 携带于 `Authorization` 头，鉴权用 |
| `refresh_token` | 长（如 7 天） | 用于换取新的 `access_token` |

**痛点：** `access_token` 可能在任何一次请求中过期（返回 `401`），如果每个页面、每个请求都单独处理「判断 401 → 调刷新接口 → 存新 token → 重试原请求」，代码会大量重复，极易遗漏或写出 bug。

**目标：** 封装一个统一的请求拦截器，一处处理，全项目生效——业务代码只用关心「调什么接口、拿什么数据」，不感知 token 的刷新细节。

---

## 二、整体架构

```
┌──────────────────────────────────────────────────┐
│  业务页面（settings / gallery / home ...）         │
│  request({ url: API.XXX, method: 'GET' })         │
│    .then(res => ...)                              │
│    .catch(err => ...)                             │
└──────────────────┬───────────────────────────────┘
                   │ 调用
                   ▼
┌──────────────────────────────────────────────────┐
│  utils/request.js  —— 请求拦截器                   │
│                                                    │
│  ① 自动挂 Authorization: Bearer <access_token>     │
│  ② 发起 wx.request                                 │
│  ③ 遇 401 → 刷新锁判断 → 调 /auth/refresh           │
│  ④ 刷新成功 → 存新 token → 重试队列                 │
│  ⑤ 刷新失败 → 清 token → 跳转登录页                 │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  后端 API                                          │
│  /auth/refresh  —— 刷新 token                      │
│  /auth/me       —— 获取用户信息                     │
│  /favorites     —— 收藏列表                        │
│  ...                                               │
└──────────────────────────────────────────────────┘
```

---

## 三、刷新锁（Refresh Lock）机制

**问题：** 同一时刻可能有多个请求同时返回 `401`（如页面加载时并发拉取了用户信息、收藏列表、图片列表），如果每个 `401` 都独立调一次 `/auth/refresh`，会产生 N 次重复刷新请求，浪费资源且可能造成竞态条件。

**方案：** 全局刷新锁 `isRefreshing` + 请求队列 `refreshQueue`。

```
并发请求 A、B、C 同时返回 401
        │
        ▼
  ┌─────────────────────┐
  │ A 先到达              │ → isRefreshing = false → 触发刷新，isRefreshing = true
  │ B、C 到达             │ → 检测到 isRefreshing = true → 只把 {options, resolve, reject} 推入 refreshQueue
  └─────────────────────┘
        │
        ▼
  刷新完成，拿到新 token
        │
   ┌────┴────┐
   │         │
  成功      失败
   │         │
   ▼         ▼
 retryQueue  failQueue
   │         │
   ▼         ▼
 A、B、C    A、B、C
 用新 token 全部 reject
 全部重试   + 跳转登录页
```

关键代码结构：

```js
// utils/request.js

let isRefreshing = false;        // 刷新锁
let refreshQueue = [];           // 等待队列

function request(options) {
  // ... 发起请求 ...

  rest.success = (res) => {
    if (res.statusCode === 401 && !skipAuth) {
      // 加入等待队列
      refreshQueue.push({ options, resolve, reject });

      // 只有第一个 401 真正触发刷新
      if (!isRefreshing) {
        isRefreshing = true;
        doRefresh()
          .then(() => retryQueue())   // 成功 → 重试全部
          .catch(() => failQueue());  // 失败 → 拒绝全部
      }
      return;
    }
    resolve(res);
  };
}
```

---

## 四、核心流程详解

### 4.1 请求发起

```
request(options)
  │
  ├─ skipAuth = true?  → 跳过，直接发请求
  │
  └─ skipAuth = false?
       │
       ├─ 从 storage 读取 access_token
       ├─ 写入 header: { Authorization: "Bearer xxx" }
       └─ 调用 wx.request
```

### 4.2 正常响应（非 401）

```
res.statusCode ≠ 401
  │
  ├─ 调用原始 success 回调（兼容旧写法）
  └─ resolve(res) → 业务层 .then() 拿到结果
```

### 4.3 401 响应

```
res.statusCode === 401（且非 skipAuth）
  │
  ├─ 将该请求的 {options, resolve, reject} 推入 refreshQueue
  │
  ├─ isRefreshing === false（我是第一个）
  │    │
  │    └─ 调用 doRefresh()
  │         │
  │         ├─ 从 storage 读取 refresh_token
  │         ├─ POST /auth/refresh { refresh_token }
  │         │
  │         ├─ 后端返回 200 + 新 token
  │         │    │
  │         │    ├─ saveTokens() → 存入 storage
  │         │    └─ resolve(新 access_token)
  │         │
  │         └─ 后端返回非 200 / 网络失败
  │              │
  │              ├─ clearAndGoLogin() → 清 storage + 跳登录页
  │              └─ reject
  │
  └─ isRefreshing === true（已有刷新进行中）
       │
       └─ 什么都不要做，安静排队等待 retryQueue / failQueue
```

### 4.4 刷新成功后重试

```
retryQueue()
  │
  ├─ 取出 refreshQueue 中所有请求
  ├─ 清空队列、重置锁
  ├─ 从 storage 读取新的 access_token
  │
  └─ 遍历每个请求：
       │
       ├─ 用新 token 替换 header.Authorization
       └─ 重新发起 wx.request → resolve/reject
```

### 4.5 刷新失败

```
failQueue()
  │
  ├─ 取出 refreshQueue 中所有请求
  ├─ 清空队列、重置锁
  │
  └─ 遍历每个请求：
       │
       └─ reject(new Error('登录已过期'))
          （此时 clearAndGoLogin 已由 doRefresh 调用）
```

---

## 五、关键函数一览

| 函数 | 位置 | 职责 |
|---|---|---|
| `request(options)` | `utils/request.js` | 核心入口，替换 `wx.request` |
| `doRefresh()` | 内部 | 调 `/auth/refresh`，返回新 token 的 Promise |
| `retryQueue()` | 内部 | 刷新成功后，用新 token 重试队列中所有请求 |
| `failQueue()` | 内部 | 刷新失败后，拒绝队列中所有请求 |
| `saveTokens(data)` | 导出为 `request.saveTokens` | 将 `access_token` / `refresh_token` / `expires_in` 存入 storage |
| `clearAndGoLogin()` | 导出为 `request.clearAndGoLogin` | 清空所有 token 并跳转登录页（带循环跳转保护） |
| `request.get()` | 便捷方法 | `request({ method: 'GET', url })` |
| `request.post()` | 便捷方法 | `request({ method: 'POST', url, data })` |
| `request.put()` | 便捷方法 | `request({ method: 'PUT', url, data })` |
| `request.delete()` | 便捷方法 | `request({ method: 'DELETE', url })` |

---

## 六、业务代码使用方式

### 6.1 需要认证的请求（自动处理 token）

```js
const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

// Promise 风格
request({ url: API.USER_INFO, method: 'GET' })
  .then(res => {
    if (res.statusCode === 200) {
      this.setData({ username: res.data.username });
    }
  })
  .catch(err => console.error('请求失败', err));

// 便捷方法
request.get(API.FAVORITE_LIST)
  .then(res => { /* ... */ });

request.post(API.FAVORITE_TOGGLE, { image_id: 'img001' })
  .then(res => { /* ... */ });
```

### 6.2 不需要认证的请求（skipAuth）

```js
// 发送验证码
request({
  url: API.SEND_CODE,
  method: 'POST',
  data: { email: 'test@qq.com' },
  skipAuth: true
});

// 登录
request({
  url: API.USER_LOGIN,
  method: 'POST',
  data: { email, code },
  skipAuth: true
}).then(res => {
  if (res.statusCode === 200) {
    request.saveTokens(res.data);  // 使用统一的 token 存储
    wx.reLaunch({ url: '/pages/home/home' });
  }
});
```

### 6.3 外部第三方 API

```js
// 不走后端、不需要 token 的纯外部接口 —— 直接用 wx.request
wx.request({
  url: 'https://t.alcy.cc/json/?pc=10',
  success: (res) => { /* ... */ }
});
```

---

## 七、改造前后对比

### app.js

**改造前（112 行）：** 手动维护 `checkLoginStatus` / `tryRefreshToken` / `clearTokenAndGoLogin`，每个方法里都要写 token 读写、401 判断、跳转保护。

**改造后（51 行）：** `tryRefreshToken` / `clearTokenAndGoLogin` 方法整段删除，`checkLoginStatus` 变成 3 行：

```js
checkLoginStatus() {
  if (!wx.getStorageSync('access_token')) return this.redirectToLogin();
  request({ url: API.USER_INFO })
    .then(res => res.statusCode === 200 ? this.redirectToHome() : this.redirectToLogin())
    .catch(() => this.redirectToLogin());
}
```

### 业务页面

**改造前：** 每次请求都要手写三段样板代码：

```js
const token = wx.getStorageSync('access_token');
if (!token) { wx.reLaunch(...); return; }
wx.request({
  url: API.XXX,
  header: { 'Authorization': `Bearer ${token}` },
  success(res) {
    if (res.statusCode === 401) {
      // 又要手动刷新 token...
    }
  }
});
```

**改造后：** 只需要：

```js
request({ url: API.XXX, method: 'GET' }).then(res => { ... });
```

---

## 八、注意事项

1. **`skipAuth` 不能滥用：** 只有登录、注册、发送验证码等入口接口才应该加 `skipAuth: true`。所有需要登录态的接口都不加，让拦截器自动处理。

2. **循环跳转保护：** `clearAndGoLogin` 已内置判断——如果当前页面已经是 `pages/login/login`，不会再重复 `reLaunch`，避免死循环。

3. **外部 API 不经过拦截器：** 像 `t.alcy.cc` 这种第三方图源，直接用 `wx.request`，不要走 `request()`。

4. **并发安全：** 同一时刻最多只有一个 `/auth/refresh` 请求在飞，其余 401 排队等结果。即使 10 个请求同时过期，也只会调一次刷新接口。

5. **兼容旧代码：** `request()` 同时支持 Promise（`.then/.catch`）和传统回调（`success/fail`），可以渐进式迁移。但推荐统一用 Promise 风格。

6. **`saveTokens` 复用：** 登录成功后调用 `request.saveTokens(res.data)` 统一存储，而非在多处重复写 `wx.setStorageSync`，保证存储逻辑只有一份实现。
