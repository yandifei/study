传递唯一值是微信小程序登录流程的核心环节。标准的做法是：**前端获取一个临时的 `code`，然后由后端将其交换成最终的用户唯一标识 `openId`**。你的后端需要先获取 `AppSecret` 密钥。

整个流程会用到两个“唯一值”，下面我们分步说明。

### 🔑 后端准备：获取你的小程序密钥（AppSecret）

这是后端进行凭证交换的“钥匙”，**绝不能放在前端代码中，必须严格保密**。

1.  登录[微信公众平台](https://mp.weixin.qq.com/)。
2.  进入 `开发` -> `开发管理` -> `开发设置`。
3.  在 `开发者ID` 区域找到 `AppSecret (小程序密钥)`，点击 `重置` 或 `生成` 后妥善保管。

---

### 第一步：小程序前端获取临时凭证 `code`

在用户触发登录时（如点击登录按钮），你需要在页面JS中调用`wx.login()`来获取一个临时的、使用时效约5分钟的 `code`。这里每个`code`仅能使用一次。

```javascript
Page({
  login() {
    wx.login({
      success: (res) => {
        // 1. 成功获取到一次性使用的临时凭证 code
        if (res.code) {
          this.sendCodeToBackend(res.code);
        } else {
          console.log('登录失败！' + res.errMsg);
        }
      }
    });
  },

  sendCodeToBackend(code) {
    // 2. 调用你的后端接口，将 code 作为参数传递
    wx.request({
      url: 'https://your-backend.com/api/login',
      method: 'POST',
      data: { code: code },
      success: (res) => {
        // 3. 接收到后端返回的最终凭证（token），并保存
        const token = res.data.token;
        wx.setStorageSync('userToken', token);
        console.log('登录成功，token已保存');
      }
    });
  }
});
```

---

### 第二步：后端服务器用 `code` 换取用户唯一标识 `openId`

这一步是整个流程的核心，你的后端需要请求微信官方的 `auth.code2Session` 接口，将 `code` 转换为真正能标识用户唯一身份的 `openId`。

```python
import requests

@app.route('/api/login', methods=['POST'])
def wechat_login():
    code = request.json.get('code')

    # 你的小程序配置信息
    app_id = 'YOUR_APP_ID'
    app_secret = 'YOUR_APP_SECRET' # 就是前面获取的那个密钥

    # 调用微信接口
    url = f'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': app_id,
        'secret': app_secret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    result = requests.get(url, params=params).json()
    
    # result 包含 openid, session_key 等
    openid = result.get('openid')
    # 如果获取openid失败，说明code已失效
    if not openid:
        return {'error': '登录失败'}, 401
        
    # 可选：生成你自己的token (如JWT)
    # your_token = generate_token(openid)
    
    return {
        'token': your_token, # 返回给你的token
        # 'openid': openid,  # 切记：不要将openid返回给前端
    }
```

**获取到的 `openid` 信息如下：**
*   **`openid`**：**用户在当前小程序下的唯一标识，这正是你要传递的“唯一值”**。你应该将这个 `openid` 与你的后端用户系统关联起来，作为该用户的登录凭证。
*   **`unionid`**：如果开发者有多个微信应用（如公众号、小程序），可通过 `unionid` 来区分用户的唯一性，它在同一开放平台下的所有应用中都是相同的。
*   **`session_key`**：用于解密用户敏感数据的会话密钥。**这个值极其重要，后端不应将其返回给前端**。

### 🛡️ 后端再加工：生成并返回你自己的登录凭证 `Token`

最后，后端在获得 `openid` 后，可以生成你自己的登录凭证返回给前端。

这个凭证通常是一个 `Token`（如 `JSON Web Token`），相较于直接返回 `openid` 更安全。前端收到后需要将它**保存在本地存储**中。

```javascript
// 示例：前端保存token
wx.setStorageSync('userToken', 'token-from-server');
```
之后前端在发起需要登录态的请求时，在请求头（Header）中带上这个 `Token`，后端解析 `Token` 就能识别是哪个用户了，从而保护后续所有的接口。