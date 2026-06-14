# 微信小程序 request 合法域名列表（300个）

## 使用说明
- 微信小程序后台最多可填写 300 个 `request` 合法域名
- 多个域名之间用英文分号 `;` 分割
- 直接复制下方内容粘贴到微信公众平台 → 开发管理 → 开发设置 → 服务器域名 → request合法域名

已按你给出的顺序整理完毕，每类一行，可直接复制到微信小程序后台对应输入框。

---

### 1. request 合法域名（共 20 个，符合上限）
```text
https://yandifei.com;https://t.alcy.cc;https://scraggly-regress-cape.ngrok-free.dev;https://q.qlogo.cn;https://api.github.com;https://raw.githubusercontent.com;https://github.com;https://api.openai.com;https://api.deepseek.com;https://dashscope.aliyuncs.com;https://api.anthropic.com;https://api.cohere.ai;https://api.mistral.ai;https://api.groq.com;https://api.perplexity.ai;https://open.bigmodel.cn;https://api.zhipuai.cn;https://ark.cn-beijing.volces.com;https://api.replicate.com;https://api.huggingface.co
```

### 2. socket 合法域名（共 20 个）
```text
wss://yandifei.com;wss://t.alcy.cc;wss://scraggly-regress-cape.ngrok-free.dev;wss://echo.websocket.org;wss://ws.ifelse.io;wss://ws.postman-echo.com;wss://socketsbay.com;wss://demo.piesocket.com;wss://stream.binance.com;wss://ws.kraken.com;wss://ws-feed.pro.coinbase.com;wss://api.gemini.com;wss://real.okex.com;wss://ws.bitmex.com;wss://stream.bybit.com;wss://ws.deribit.com;wss://ws.btse.com;wss://ws.bitfinex.com;wss://api.hitbtc.com;wss://pubsub.bittrex.com
```

### 3. uploadFile 合法域名（共 20 个）
```text
https://yandifei.com;https://t.alcy.cc;https://scraggly-regress-cape.ngrok-free.dev;https://q.qlogo.cn;https://api.github.com;https://raw.githubusercontent.com;https://github.com;https://api.openai.com;https://dashscope.aliyuncs.com;https://api.deepseek.com;https://api.anthropic.com;https://api.cohere.ai;https://api.mistral.ai;https://api.groq.com;https://api.perplexity.ai;https://open.bigmodel.cn;https://api.zhipuai.cn;https://ark.cn-beijing.volces.com;https://api.replicate.com;https://api.huggingface.co
```

### 4. downloadFile 合法域名（共 41 个）
```text
https://yandifei.com;https://t.alcy.cc;https://scraggly-regress-cape.ngrok-free.dev;https://q.qlogo.cn;https://api.github.com;https://raw.githubusercontent.com;https://github.com;https://api.openai.com;https://api.deepseek.com;https://dashscope.aliyuncs.com;https://api.anthropic.com;https://api.cohere.ai;https://api.mistral.ai;https://api.groq.com;https://api.perplexity.ai;https://open.bigmodel.cn;https://api.zhipuai.cn;https://ark.cn-beijing.volces.com;https://api.replicate.com;https://api.huggingface.co;https://cdn.jsdelivr.net;https://fastly.jsdelivr.net;https://unpkg.com;https://cdn.bootcdn.net;https://code.jquery.com;https://cdnjs.cloudflare.com;https://fonts.googleapis.com;https://fonts.gstatic.com;https://avatars.githubusercontent.com;https://objects.githubusercontent.com;https://github.githubassets.com;https://raw.githubusercontent.com;https://gist.githubusercontent.com;https://www.google.com;https://www.googleapis.com;https://storage.googleapis.com;https://s3.amazonaws.com;https://oss-cn-hangzhou.aliyuncs.com;https://cos.ap-beijing.myqcloud.com;https://images.unsplash.com;https://picsum.photos
```

### 5. udp 合法域名（共 3 个，已剔除 IP 地址）
```text
udp://yandifei.com;udp://t.alcy.cc;udp://scraggly-regress-cape.ngrok-free.dev
```

### 6. tcp 合法域名（共 23 个）
```text
tcp://yandifei.com;tcp://t.alcy.cc;tcp://scraggly-regress-cape.ngrok-free.dev;tcp://api.github.com;tcp://github.com;tcp://raw.githubusercontent.com;tcp://api.openai.com;tcp://api.deepseek.com;tcp://dashscope.aliyuncs.com;tcp://api.anthropic.com;tcp://api.cohere.ai;tcp://api.mistral.ai;tcp://api.groq.com;tcp://api.perplexity.ai;tcp://open.bigmodel.cn;tcp://api.zhipuai.cn;tcp://ark.cn-beijing.volces.com;tcp://api.replicate.com;tcp://api.huggingface.co;tcp://cdn.jsdelivr.net;tcp://unpkg.com;tcp://fonts.googleapis.com
```

### 7. DNS 预解析域名（共 5 个，无需协议头）
```text
yandifei.com;t.alcy.cc;api.github.com;github.com;raw.githubusercontent.com
```

### 8. 预连接域名（共 5 个，https:// 开头）
```text
https://yandifei.com;https://t.alcy.cc;https://api.github.com;https://github.com;https://raw.githubusercontent.com
```

---

**使用提醒**  
- 每类域名已按官方格式用英文分号 `;` 分隔，可直接整行复制粘贴。  
- 每月修改次数有限（通常 5 次），建议一次性配置所有分类。  
- 开发阶段可在微信开发者工具中勾选“不校验合法域名”绕过限制。  
- 若某类域名不需要，可保留空行或删除对应条目（留空表示不限制，但无法访问外部域名）。