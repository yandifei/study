由于服务器拥有公网IP，设置 Token 鉴权是保护服务的第一步。下面分别梳理 **NapCat**、**AstrBot** 和 **gsuid_core** 这三个服务相关的 Token 及安全配置。
---

## 一、NapCat 安全配置

### 1. WebUI 初始登录 Token（获取位置）

NapCat 启动后会在日志中生成 WebUI 登录所需的随机 Token，需要在浏览器输入该 Token 才能进入管理界面：

```bash
docker logs napcat 2>&1 | grep -i "WebUi.*token"
```

日志中会显示类似：

```
[WebUi] WebUi User Panel Url: http://127.0.0.1:6099/webui?token=xxxxx
```

其中 `xxxxx` 即为 Token。

或者直接查看配置文件 `./napcat/config/webui.json`（若未生成则需等容器完整启动一次），其中 `"token"` 字段即为登录凭证。

访问 `http://<你的公网IP>:6099/webui?token=<上面获得的Token>` 即可进入 WebUI。

> 登录后系统会**强制要求修改密码**，否则大部分功能将被禁用——请务必完成此项操作。

> ⚠️ **安全提示**：NapCat 的 WebUI 登录 Token **禁止与他人分享**，否则任何人都可以登录并控制你的机器人配置。公网部署时建议将 `webui.json` 中的 `host` 从 `0.0.0.0` 修改为 `127.0.0.1`，仅允许本地访问 WebUI，再通过反向代理（如 nginx）以 HTTPS 方式对外暴露访问，同时启用基本认证或 IP 白名单限制。

### 2. WebSocket 客户端 Token（创建时获取，用于 AstrBot 对接）

AstrBot 需要以 **WebSocket 客户端** 模式连接 NapCat（即 AstrBot 主动连接 NapCat 的 `/ws` 端点）。在 NapCat WebUI 内完成“扫码登录 QQ”后，按以下步骤操作：

1. 进入 NapCat WebUI → **网络配置** → 点击 **新建**。
2. 类型选择 **WebSocket 客户端**。
3. 填写：
   - **名称**：可任意填写（如 `astrbot`）。
   - **URL**：填写 `ws://astrbot:4141/ws` 或 `ws://host.docker.internal:4141/ws`（取决于通信方向，下面会详细说明）。
   - **心跳间隔**：建议 `5000`，**重连间隔**：建议 `5000`。
4. **重要**：勾选 **启用 Token 认证**，然后点击保存。此时会生成一个 **Token 字符串**，**请务必记录**。该 Token 就是连接时的 `accessToken`。

这个 **WebSocket 认证 Token** 需要填写到 AstrBot 的消息平台配置中，详见第二部分。

### ⚠️ 方向说明：WebSocket 客户端 vs 服务器——哪种适合你？

WebSocket 通信有两种主流模式，你需要理解其区别才能正确配置：

| 方向                                | 谁主动连接谁            | NapCat 中的配置类型                       | AstrBot 中的配置                 |
| ----------------------------------- | ----------------------- | ----------------------------------------- | -------------------------------- |
| **NapCat 正向连接 AstrBot**（推荐） | NapCat 主动连接 AstrBot | **WebSocket 客户端**（NapCat 作为客户端） | 配置端口监听即可，不填额外 Token |
| **AstrBot 正向连接 NapCat**（备选） | AstrBot 主动连接 NapCat | **WebSocket 服务器**（NapCat 作为服务端） | 配置 `ws://…` 地址和 Token       |

此处以最常用的 **推荐方案**（NapCat 主动连接 AstrBot）为准进行说明。如果你的业务场景有其他需求，可以按上表对应调整。

### 推荐：NapCat 正向连接 AstrBot

如果你想让 **NapCat 主动连接 AstrBot**（推荐方式，减少 AstrBot 被第三方恶意连接的风险）：

- **NapCat 网络配置**：选择 **WebSocket 客户端**，URL 填写 `ws://astrbot:4141/ws`（或 `ws://主机IP:4141/ws`），填写上面记录的 WebSocket Token，点击保存。
- **AstrBot 配置**：在 AstrBot → **消息平台** → 新增 **接入 QQ 个人号** 时，填写的信息见下文。

> 如果你的 AstrBot 和 NapCat 运行在同一个 Docker Compose 项目中（就像你的 `docker-compose.yaml` 配置的那样），在 `astrbot_network` 这个自定义网络内，直接用容器名 `astrbot` 作为主机名即可——`ws://astrbot:4141/ws`。不需要使用 `host.docker.internal` 或公网 IP。

> 这种方式下，AstrBot 不需要在消息平台侧额外填写 Token，因为**接入 QQ 个人号时填写的 Token 正是用于校验 NapCat 发来的 WebSocket 请求**。只要两边 Type/Token 一致，连接即可建立。

### 备选：AstrBot 正向连接 NapCat

如果你的网络环境要求 AstrBot 必须主动连接 NapCat，也可以反向配置：

- **NapCat 网络配置**：选择 **WebSocket 服务器**，监听地址填写 `/ws` 路径，**必须**勾选启用 Token 认证并记录生成的 Token。
- **AstrBot 配置**：在消息平台设置中，将 URL 指向 NapCat，并**在消息平台配置中填入相同的 Token**。

两种方式均可正常工作，选择更符合你网络架构的一种即可。本文以 **第一种（NapCat 主动连接 AstrBot）为主** 进行描述。

### 3. 公网暴露时的代理层安全

**强烈建议**：不要将 NapCat WebUI（`6099` 端口）直接暴露在公网。如果确实需要公网访问，请在前方加一层反向代理（如 nginx），配置 HTTPS、基本认证（`Authorization: Basic`）并限定 IP 白名单。

---

## 二、AstrBot 安全配置

### 1. AstrBot Dashboard 的访问密码

默认账号密码均为 `astrbot`。如果希望修改，可进入 AstrBot WebUI → **设置** → **账号管理**（或者在运行容器后修改 `./astrbot-data/cmd_config.json` 中的 `dashboard.username` 和 `dashboard.password` 字段）。密码存储经过 MD5 加密。

### 🔐 安全要点：禁用默认管理员账号并创建独立的管理员

默认账号密码为 `astrbot`/`astrbot`，**这是公开的默认凭证，必须修改或禁用**。参考以下操作：

1. **立即修改默认密码**：登录 WebUI 后前往 **设置** → **账号管理**，修改 `astrbot` 账户的密码。
2. **创建独立的管理员账户**：在 **账号管理** 中添加一个新管理员账号，使用高强度密码，并将你的 QQ 号在 **配置** → **其他配置** → **管理员 ID 列表** 中加入。
3. **锁定或删除默认的 `astrbot` 账户**：在确认新管理员账户可用之后，修改默认账户的密码为一个随机长字符串并保存，确保无法被猜测或直接使用。
4. **关闭 HTTP 基本认证中的默认凭据（如有）**：如果你在反代层额外配置了 HTTP Basic Auth，请确保不使用 `astrbot`/`astrbot` 作为基本认证凭据。

### 2. 与 NapCat 对接：配置“接入 QQ 个人号”适配器

在 AstrBot WebUI 中执行以下操作：

1. 进入 **消息平台** → 点击 **+** 号选择 **接入 QQ 个人号**。
2. **启用** 开关打开。
3. **WebSocket Token** 处，直接填入你在上面 NapCat WebSocket 客户端创建时记录的 Token。
4. **Type** 选择 `ws` 方向。
5. 点击 **保存并启用**。

### 3. AstrBot Agent 沙箱（Shipyard Neo）的 Access Token

在你的 `docker-compose.yaml` 中，AstrBot 使用了 Bay 作为沙箱环境驱动器。Bay 的 `config.yaml` 中配置了 `security.api_key`（安全要求的固定 API Key）。**两者必须保持一致**。

配置步骤如下（参照原一体化指南文档）：

1. 在 `config.yaml` 中设置一个强随机 Token，例如：
   ```yaml
   security:
     api_key: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"  # 这是一个示例，请自行生成更强的随机字符串
   ```
   推荐使用 `openssl rand -hex 32` 生成 64 位十六进制随机数，确保足够安全。
2. **将 `api_key` 填入 AstrBot**：
   - 进入 AstrBot → **AI 配置** → **Agent Computer Use**。
   - Endpoint 填写 `http://bay:8114`（已在同一 `astrbot_network` 中）。
   - **Access Token** 处填写与 `security.api_key` **完全相同**的值。
3. 点击保存，AstrBot 即可通过这个 Token 访问 Bay 的沙箱 API。

> 注意：此 Token 与第二节中的 WebSocket Token **是两条完全独立的 Token**，不要混淆。

---

## 三、早柚核心（gsuid_core）安全配置

### 1. 网页控制台的注册码（REGISTER_CODE）

`config.json` 位于 `./gsuid_core/data/config.json`。首次运行 gsuid_core 容器后该文件会自动生成。在其中找到 `REGISTER_CODE` 字段，该字段值即为注册码。

```json
"REGISTER_CODE": "4e8cd750c93de5c5"
```

复制该值后，在浏览器打开 `http://<你的公网IP>:8765/app/` 进行注册：

- 用户名建议使用你的 QQ 号（便于后续权限管理）。
- 注册码字段粘贴上述值。
- 设置一个高强度的登录密码（不要与 Token 重复使用）。

> ✅ **安全提示**：注册成功并登录后，建议立即**修改 `REGISTER_CODE`** 为一个新的随机字符串并重新保存 `config.json`，防止他人再次利用已知注册码创建额外账号。恢复操作时可通过进入容器修改 `config.json` 或通过网页控制台的“安全设置”修改注册码并重启容器。

### 2. WebSocket Token（WS_TOKEN）

gsuid_core 与 AstrBot 通过 WebSocket 通信，需要通过 WS_TOKEN 进行鉴权。

**第一步：在 core 端配置 WS_TOKEN**

- 方式一（推荐）：进入 gsuid_core WebUI（`http://<公网IP>:8765/app/`），在左侧 **Core 配置** 标签页中找到 `WS_TOKEN` 字段，直接修改并保存。
- 方式二：直接编辑 `./gsuid_core/data/config.json`，找到 `WS_TOKEN` 字段，填入一个强随机字符串。默认值为空字符串（`""`）表示仅允许来自本机的连接，若 AstrBot 和 gsuid_core 运行在不同容器中——**即使在同一 Docker Compose 项目中，跨容器调用也必须配置 WS_TOKEN，不能留空**。

   示例：
   ```json
   "WS_TOKEN": "sk-7x9m2q4w6y8a0b1c2d3e4f5g6h7i8j9k"
   ```

修改后需要重启 gsuid_core 容器：

```bash
docker-compose restart gsuid_core
```

**第二步：在 AstrBot 端配置相同的 WS_TOKEN**

在 AstrBot WebUI → **已安装插件** 中找到 `astrbot_plugin_gscore_adapter`，点击配置：

- **Core Host**：填写 `ws://host.docker.internal:8765`（如果 AstrBot 和 gsuid_core 在同一个 Docker 网络中，也可使用容器名 `ws://gsuid_core:8765`）。
- **WS_TOKEN**：填入与上一步相同的 Token 字符串。
- 保存并重启插件。

> 关于 WS_TOKEN 的更详细安全配置，可参考早柚官方安全文档和 WebSocket Token 配置说明。

---

## 四、Token 管理与安全最佳实践

### 1. Token 的存储与保护

- **不要将 Token 硬编码在 `docker-compose.yaml` 的 `environment` 或 `volumes` 路径中**——环境变量会出现在 `docker inspect` 或 `docker-compose config` 的输出中，属于不安全的做法。若必须通过环境变量传递，建议使用 `.env` 文件并严格限制文件权限（`chmod 600 .env`），并确保 `.env` 不被 Git 提交（加入 `.gitignore`）。
- 每个 Token 使用不同的随机字符串，避免复用。
- 定期轮换 Token（每 90 天或根据安全策略）。
- 使用密码管理器保存 Token，不要直接写在笔记/文档中。
- 若多人维护，在 CI/CD 或部署脚本中使用秘密管理工具（如 HashiCorp Vault、Infisical 或 Docker Secret）来管理敏感信息。

### 2. 公网部署时的额外防护

- 为所有 Web 服务启用 HTTPS（自签名证书不安全，建议使用 Let's Encrypt）。
- 为 WebUI（AstrBot `6185` 端口、gsuid_core `8765` 端口）配置反向代理 + 基本认证（Authentication），并设置 IP 白名单。
- 为 NapCat WebUI 配置 `webui.json` 中的 `host: "127.0.0.1"`，并通过本地反向代理（如 caddy）限制暴露范围。
- 监控日志，及时发现异常访问或频繁尝试。

### 3. 立即执行的优先级清单

| 优先级 | 操作                       | 说明                                     |
| ------ | -------------------------- | ---------------------------------------- |
| 🔴 高   | 修改 NapCat WebUI 登录密码 | 登录后强制完成，否则功能受限             |
| 🔴 高   | AstrBot 默认管理员密码     | 立即修改或删除默认 `astrbot` 账户        |
| 🔴 高   | gsuid_core 注册码          | 首次登录成功后，立即更改 `REGISTER_CODE` |
| 🟡 中   | NapCat WebSocket Token     | 创建时记录，用于 AstrBot 客户端配置      |
| 🟡 中   | gsuid_core WS_TOKEN        | 两端配置一致的随机 Token                 |
| 🟡 中   | AstrBot gscore 插件        | 填入正确的 Core Host 和 WS_TOKEN         |
| 🟢 低   | 定期轮换 Token             | 按计划周期更换密钥（建议每 30~90 天）    |

---

## 五、快速检查清单

启动所有服务后，按照以下列表逐一检查，确保所有 Token 均正确配置且生效：

- [ ] NapCat：WebUI 使用日志 Token 可以正常登录且已修改密码。
- [ ] NapCat：**WebSocket 客户端**已创建并启用 Token 认证，URL 指向 AstrBot。
- [ ] AstrBot：已添加“接入 QQ 个人号”适配器，Token 与 NapCat 的一致。
- [ ] AstrBot：已重置默认管理员密码，或设置独立管理员账户并锁定默认账户。
- [ ] AstrBot：沙箱（Agent Computer Use）的 Access Token 与 Bay 的 `api_key` 严格一致。
- [ ] gsuid_core：使用 `REGISTER_CODE` 注册成功，且注册码已更新。
- [ ] gsuid_core：`WS_TOKEN` 已配置非空值，且已重启生效。
- [ ] AstrBot gscore 插件：Core Host 填写正确，WS_TOKEN 与 core 端一致。
- [ ] 可选：代理层（如有）已启用 HTTPS 和基本认证。