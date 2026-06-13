Dify的源码官网：https://github.com/langgenius/dify

官方中文文档：https://docs.dify.ai/zh/use-dify/getting-started/introduction

--- 

**不要研究源码，先部署起来。**

贴出来的这个 `.env`，对于第一次部署来说，**99% 不用改**。

---

## 最简单部署

```bash
git clone https://github.com/langgenius/dify.git

cd dify/docker

cp .env.example .env

docker compose up -d
```

就这么干。

---

## 哪些必须改？

实际上第一次部署只建议改 2 个。

### 1. INIT_PASSWORD

找到：

```env
INIT_PASSWORD=
```

改成：

```env
INIT_PASSWORD=你的管理员密码
```

例如：

```env
INIT_PASSWORD=Admin@123456
```

这样第一次登录后台不用邮件注册。

---

### 2. DeepSeek/OpenAI Key

这个不用在 `.env` 配。

部署完成后：

```text
http://服务器IP
```

登录后台。

然后：

```text
Settings
  ↓
Model Provider
  ↓
OpenAI
DeepSeek
Claude
Gemini
```

在网页里填。

---

## 哪些不用动？

### 数据库

```env
DB_USERNAME=postgres
DB_PASSWORD=difyai123456
```

不用动。

因为：

```text
Postgres
Redis
Weaviate
```

都在 Docker 网络内部。

外面访问不到。

---

### Redis

```env
REDIS_PASSWORD=difyai123456
```

不用动。

---

### 向量数据库

```env
VECTOR_STORE=weaviate
```

不用动。

Dify 自己管理。

---

### Secret Key

```env
SECRET_KEY=
```

甚至可以不填。

Dify 第一次启动会自动生成。

---

## 哪些是公网部署才改？

例如：

```env
CONSOLE_API_URL=
CONSOLE_WEB_URL=
APP_API_URL=
APP_WEB_URL=
```

本地测试：

全部不用管。

---

如果未来部署：

```text
https://ai.xxx.com
```

才改：

```env
CONSOLE_WEB_URL=https://ai.xxx.com
```

之类。

---

## 你的流程应该是

### 第一步

启动：

```bash
docker compose up -d
```

看容器：

```bash
docker ps
```

应该有：

```text
dify-api
dify-web
postgres
redis
weaviate
sandbox
plugin-daemon
```

---

### 第二步

浏览器：

```text
http://localhost
```

或者：

```text
http://服务器IP
```

看到 Dify 登录页。

---

### 第三步

配置模型

例如 DeepSeek：

```text
Settings
 ↓
Model Provider
 ↓
DeepSeek
```

填：

```text
API Key
```

即可。

---

### 第四步

创建应用

```text
Studio
 ↓
Create App
 ↓
Chatflow
```

创建：

```text
我的AI助手
```

---

### 第五步

拿 API Key

应用里面：

```text
API Access
```

会看到：

```text
App Key
```

类似：

```text
app-xxxxxxxxxxxxxxxx
```

---

### 第六步

前端调用

```javascript
await fetch(
  "http://你的服务器/v1/chat-messages",
  {
    method: "POST",
    headers: {
      Authorization: "Bearer app-xxxx",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query: "你好",
      user: "test"
    })
  }
);
```

就能聊天了。

---

我建议你现在先执行：

```bash
docker compose up -d
```

如果启动报错，把你的：

```bash
docker compose ps

docker compose logs api
```

结果发给我。

我可以直接帮你判断是：

* Docker 问题
* 内存不足
* 端口冲突
* 镜像拉取失败
* Apple Silicon/M系列芯片问题

还是 Dify 配置问题。这样比研究那几百个环境变量高效得多。
