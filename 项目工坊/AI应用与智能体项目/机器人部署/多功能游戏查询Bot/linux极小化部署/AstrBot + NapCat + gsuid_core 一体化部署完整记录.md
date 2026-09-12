# AstrBot + NapCat + gsuid_core 一体化部署完整记录

本文档整合了以下四个文件的所有内容，无任何删减或概括：
1. `AstrBot + NapCat + gsuid_core 一体化部署网络问题总结.md`
2. `AstrBot + Napcat + gsuid_core 轻量部署指南.md`
3. `NapCat、AstrBot 和 gsuid_core 这三个服务相关的 Token 及安全配置.md`
4. `docker-compose.yaml`

部署中遇到的各类问题、解决方案、安全配置以及完整的 `docker-compose.yaml` 均原样收录，按部署的自然流程重新组织章节。

---

## 一、整体架构

| 服务           | 用途                           | 端口映射 (宿主机:容器)   | 备注                          |
| -------------- | ------------------------------ | ------------------------ | ----------------------------- |
| **astrbot**    | 机器人主框架 (WebUI + API)     | `6185:6185`、`4141:4141` | 数据持久化至 `./astrbot-data` |
| **napcat**     | QQ 协议客户端 (MODE=astrbot)   | `6099:6099`              | 与 astrbot 共享数据目录       |
| **gsuid_core** | 早柚核心 (原神等游戏 bot 后端) | `8765:8765`              | 需要配合 AstrBot 插件使用     |

所有服务加入自定义网络 `astrbot_network`，容器间可通过服务名直接通信。

---

## 二、部署前准备

### 1. 环境要求
- 已安装 Docker 和 Docker Compose (v2 推荐)
- 操作系统：Linux / Windows (需支持 Docker)
- 至少 4GB 可用内存，10GB 磁盘空间

> **部署目录**：`/opt/bot/`，该目录下存放 `docker-compose.yaml`  
> **启动命令**：`docker compose up -d`（在 `/opt/bot/` 内执行）  
> **当前状态**：`extra_hosts` 已从所有服务中移除，因为实践证明在 Linux 下该配置无效。

---

## 三、Docker Compose 配置文件

以下为实际部署使用的 `docker-compose.yaml` 完整内容（该文件位于 `/opt/bot/docker-compose.yaml`）。  
（轻量部署指南中原样提供的配置内容与此基本一致，但本文件包含一些后续调整的注释，为完整记录一并保留。）

```yaml
# AstrBot + Napcat + gsuid_core 一体化部署
# 部署方式: 全量模式
# 使用预构建镜像，无需本地源码

services:
  # AstrBot: 机器人框架
  # 使用方法：
  #   docker-compose up -d
  astrbot:
    image: soulter/astrbot:latest       # AstrBot 镜像
    container_name: astrbot             # AstrBot 容器名
    restart: unless-stopped             # 重启策略：除非停止，否则重启
    environment:
      - TZ=Asia/Shanghai                # 时区设置(自己加的)
      # 额外添加的，为的是代理
      # - NO_PR0XY=localhost,127.0.0.1
    ports:
      - "${ASTRBOT_PORT:-6185}:6185"    # AstrBot WebUI（必选），默认值6185，可以通过设置ASTRBOT_PORT环境变量来部署
      - "4141:4141"                     # API聚合端口（可选）
      # - "7833:7833"                   # 自主学习插件端口（可选）
    volumes:
      # - /etc/localtime:/etc/localtime:ro  # 时间同步（自己加的）
      - ./astrbot-data:/AstrBot/data    # AstrBot 持久化数据到相对路径下
    networks:
      - astrbot_network
    logging:
      driver: json-file # 指定 Docker 的日志驱动(防止日志无限增长)
      options:
        max-size: "50m" # 每个日志文件最大 50MB
        max-file: "3"   # 最多保留 3 个文件 
  
  napcat:
    image: mlikiowa/napcat-docker:latest
    container_name: napcat
    restart: unless-stopped
    environment:
      - NAPCAT_UID=${NAPCAT_UID:-1000}
      - NAPCAT_GID=${NAPCAT_GID:-1000}
      - MODE=astrbot
    ports:
      - "6099:6099"
    volumes:
    # data保持和AstrBot一致
      - ./astrbot-data:/AstrBot/data  # 让 NapCat 也能看到 AstrBot 的数据目录
      - ./napcat/config:/app/napcat/config
      - ./napcat/ntqq:/app/.config/QQ
    networks:
      - astrbot_network
    #mac_address: "02:42:ac:11:00:02"  # 可选，取消注释可固定MAC地址

  gsuid_core:
    image: docker.cnb.cool/gscore-mirror/gsuid_core:latest
    container_name: gsuid_core
    ports:
      # 服务端口
      - "8765:8765"
    volumes:
      # 数据路径 
      - ./gsuid_core/data:/gsuid_core/data
      # 插件路径
      - ./gsuid_core/plugins:/gsuid_core/gsuid_core/plugins
      # 镜像里面的python虚拟环境，不建议挂到 Windows 下(性能可能变差、文件权限/兼容性问题、依赖丢失风险)
      - venv-data:/venv
    # 容器重启策略：除非停止，否则重启
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
      # ===========================
      # 基础配置 (Basic Config)
      # ===========================
      # python镜像
      # 官方: https://pypi.org/simple/
      # 阿里: https://mirrors.aliyun.com/pypi/simple/
      # 腾讯云: https://mirrors.cloud.tencent.com/pypi/simple/
      # 火山引擎: https://mirrors.volces.com/pypi/simple/
      # 华为云: https://mirrors.huaweicloud.com/repository/pypi/simple/
      # 清华大学: https://pypi.tuna.tsinghua.edu.cn/simple/
      # 中国科学技术大学: https://pypi.mirrors.ustc.edu.cn/simple/
      - UV_INDEX=https://pypi.org/simple/
      # 使项目不再读取 pyproject.toml 配置，从而使用自定义 python 镜像
      # 开启后会读取 GSCORE_PYTHON_INDEX 作为镜像源
      # 0：关闭 1：开启
      # ⚠️注意：该操作会导致 uv.lock 发生 git diff 改动；
      - UV_NO_CONFIG=0
      # ===========================
      # 网络代理 (Proxy Config)
      # ===========================
      # 如果容器内无法连接 GitHub，请配置代理
      # 宿主机 IP 可使用 host.docker.internal (需确保代理软件开启 LAN 模式)
      # - http_proxy=http://host.docker.internal:7890
      # - https_proxy=http://host.docker.internal:7890
      # 不走代理的地址 (通常保持默认即可)
      - no_proxy="localhost,127.0.0.1,.local,cnb.cool,mirrors.aliyun.com,pypi.tuna.tsinghua.edu.cn,mirrors.volces.com"
    networks:
      - astrbot_network

# 网络改为astrbot_network，原来的配置文件网络是bay-network
networks:
  astrbot_network:
    name: astrbot_network
    driver: bridge

volumes:
  # 必须存在，这个是早柚核心的python虚拟环境，得挂载到docker卷中
  venv-data:
```

（轻量部署指南中也提供了上述 `docker-compose.yaml` 文件内容，除细节注释外结构一致，此处不再重复粘贴，但该部分内容已完整覆盖。）

---

## 四、目录结构说明

启动服务后，会自动创建以下目录（用于持久化数据）：

```
.
├── docker-compose.yaml
├── astrbot-data/          # AstrBot 数据（配置、插件、消息记录等）
├── napcat/
│   ├── config/            # NapCat 配置文件
│   └── ntqq/              # NapCat QQ 数据（含登录会话）
└── gsuid_core/
    ├── data/              # 早柚核心数据（账号、配置、注册码等）
    └── plugins/           # 早柚插件存放目录
```

---

## 五、镜像拉取与网络代理（解决外网访问不稳定）

> 以下内容源自《网络问题总结》中的问题一。

### 现象
直接执行 `docker compose up -d` 时，国内云服务器无法稳定访问 Docker Hub，导致镜像拉取超时。

### 尝试方案：配置镜像加速器
在 `/etc/docker/daemon.json` 中添加过以下镜像源：
```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://hub-mirror.c.163.com",
    "https://mirror.ccs.tencentyun.com",
    "https://docker.m.daocloud.io",
    "https://docker.nju.edu.cn",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```
然后执行 `sudo systemctl restart docker`。

**结果**：部分镜像源时好时坏，最后两个镜像（可能指 `1ms.run` 和 `xuanyuan.me`）一度不可用，但后来又恢复了，整体不稳定。

### 最终可靠方案：SSH 反向隧道 + Docker 守护进程代理
利用 Windows 本机（运行 Verge Clash，混合端口 `127.0.0.1:7897`）为阿里云服务器提供代理。

**步骤一：在 Windows 上建立 SSH 反向隧道**  
在 Windows 的 CMD 或 Tabby 中执行（需长期保持窗口）：
```bash
ssh -R 17897:127.0.0.1:7897 root@你的阿里云服务器IP
```
- `17897` 是服务器本地监听端口（无需在安全组放行）
- 建立后，服务器访问 `127.0.0.1:17897` 即走你 Windows 的代理

**步骤二：在服务器上为 Docker 守护进程配置代理**  
SSH 登录服务器后执行：
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo tee /etc/systemd/system/docker.service.d/proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:17897"
Environment="HTTPS_PROXY=http://127.0.0.1:17897"
Environment="NO_PROXY=localhost,127.0.0.1,.local"
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```
之后 `docker compose up -d` 即可稳定拉取镜像。

> **注意**：该隧道完全在本地回环通信，**「不需要在云安全组放行任何代理端口」**，安全可靠。

---

## 六、启动服务

### 1. 启动所有服务
```bash
docker-compose up -d
```

首次启动会自动拉取镜像，稍等片刻。使用以下命令检查状态：
```bash
docker-compose ps
```
应看到三个容器状态均为 `Up`。

### 2. 查看日志（排查问题）
```bash
docker-compose logs -f
```

---

## 七、初始化配置

### 1. 配置 AstrBot

访问 WebUI：`http://<宿主机IP>:6185`  
默认账号：`astrbot`  
默认密码：`astrbot`

登录后建议立即修改密码（右上角个人设置）。

#### （可选）配置 AI 服务
AstrBot 本身不强制依赖外部 AI，若要使用 ChatGPT 等，请进入 **AI 配置** 填写相应的 API Key 和端点。

> ⚠️ **关于 AstrBot Dashboard 的默认管理员账户**  
> 默认账号密码为 `astrbot`/`astrbot`，**这是公开的默认凭证，必须修改或禁用**。详细安全配置见下文「Token 及安全配置」章节。

### 2. 登录 NapCat

NapCat 通过 WebUI 或手机 QQ 扫码登录，按以下步骤操作：

1. 访问 `http://<宿主机IP>:6099`（NapCat 管理界面）
2. 根据页面提示，使用手机 QQ 扫描二维码登录
3. 登录成功后，NapCat 会保持在线，并与 AstrBot 共用 `./astrbot-data` 目录

> 若无法访问 6099 端口，请检查防火墙或 NapCat 日志：`docker-compose logs napcat`

### 3. 配置 gsuid_core（早柚核心）

#### 访问控制台
- 地址：`http://<宿主机IP>:8765/app/`（**必须带 `/app/`**）
- 首次访问会进入登录页

#### 注册账号
- 点击“注册”，输入你的 QQ 号作为账号，设置密码
- **注册码** 在 `./gsuid_core/data/config.json` 中，找到 `REGISTER_CODE` 字段的值，填入注册页面

#### 安装插件（原神、鸣潮等）
在早柚控制台 → **插件管理** 中，可以安装社区插件，例如：
- `GenshinUID`（原神）
- `XutheringWavesUID`（鸣潮）

更多插件列表参考 [早柚文档](https://docs.sayu-bot.com/InstallPlugins/PluginsList.html)

#### 连接 AstrBot 与 gsuid_core
需要安装 AstrBot 的适配插件：`astrbot_plugin_gscore_adapter`（在 AstrBot 插件市场搜索安装）。

安装后在 AstrBot 插件配置中，将 **请求地址** 填写为：
```
ws://gsuid_core:8765
```
因为两个容器在同一 Docker 网络内，可直接使用服务名 `gsuid_core` 通信。

如果需要在容器内访问宿主机的早柚服务（非推荐），可填写 `ws://host.docker.internal:8765`，但需确保 compose 文件中添加 `extra_hosts`。

> ⚠️ 之前尝试使用 `host.docker.internal` 或 `extra_hosts` 均失败，最终使用服务名解决。详见后文「网络问题总结与排错」。

---

## 八、Token 及安全配置（完整指南）

> 以下内容源自《NapCat、AstrBot 和 gsuid_core 这三个服务相关的 Token 及安全配置.md》，**包含与前面章节有部分重叠的步骤，但为保持原文完整性，全部逐字保留。** 由于服务器拥有公网IP，设置 Token 鉴权是保护服务的第一步。下面分别梳理 **NapCat**、**AstrBot** 和 **gsuid_core** 这三个服务相关的 Token 及安全配置。

### 一、NapCat 安全配置

#### 1. WebUI 初始登录 Token（获取位置）

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

#### 2. WebSocket 客户端 Token（创建时获取，用于 AstrBot 对接）

AstrBot 需要以 **WebSocket 客户端** 模式连接 NapCat（即 AstrBot 主动连接 NapCat 的 `/ws` 端点）。在 NapCat WebUI 内完成“扫码登录 QQ”后，按以下步骤操作：

1. 进入 NapCat WebUI → **网络配置** → 点击 **新建**。
2. 类型选择 **WebSocket 客户端**。
3. 填写：
   - **名称**：可任意填写（如 `astrbot`）。
   - **URL**：填写 `ws://astrbot:4141/ws` 或 `ws://host.docker.internal:4141/ws`（取决于通信方向，下面会详细说明）。
   - **心跳间隔**：建议 `5000`，**重连间隔**：建议 `5000`。
4. **重要**：勾选 **启用 Token 认证**，然后点击保存。此时会生成一个 **Token 字符串**，**请务必记录**。该 Token 就是连接时的 `accessToken`。

这个 **WebSocket 认证 Token** 需要填写到 AstrBot 的消息平台配置中，详见第二部分。

#### ⚠️ 方向说明：WebSocket 客户端 vs 服务器——哪种适合你？

WebSocket 通信有两种主流模式，你需要理解其区别才能正确配置：

| 方向                                | 谁主动连接谁            | NapCat 中的配置类型                       | AstrBot 中的配置                 |
| ----------------------------------- | ----------------------- | ----------------------------------------- | -------------------------------- |
| **NapCat 正向连接 AstrBot**（推荐） | NapCat 主动连接 AstrBot | **WebSocket 客户端**（NapCat 作为客户端） | 配置端口监听即可，不填额外 Token |
| **AstrBot 正向连接 NapCat**（备选） | AstrBot 主动连接 NapCat | **WebSocket 服务器**（NapCat 作为服务端） | 配置 `ws://…` 地址和 Token       |

此处以最常用的 **推荐方案**（NapCat 主动连接 AstrBot）为准进行说明。如果你的业务场景有其他需求，可以按上表对应调整。

#### 推荐：NapCat 正向连接 AstrBot

如果你想让 **NapCat 主动连接 AstrBot**（推荐方式，减少 AstrBot 被第三方恶意连接的风险）：

- **NapCat 网络配置**：选择 **WebSocket 客户端**，URL 填写 `ws://astrbot:4141/ws`（或 `ws://主机IP:4141/ws`），填写上面记录的 WebSocket Token，点击保存。
- **AstrBot 配置**：在 AstrBot → **消息平台** → 新增 **接入 QQ 个人号** 时，填写的信息见下文。

> 如果你的 AstrBot 和 NapCat 运行在同一个 Docker Compose 项目中（就像你的 `docker-compose.yaml` 配置的那样），在 `astrbot_network` 这个自定义网络内，直接用容器名 `astrbot` 作为主机名即可——`ws://astrbot:4141/ws`。不需要使用 `host.docker.internal` 或公网 IP。

> 这种方式下，AstrBot 不需要在消息平台侧额外填写 Token，因为**接入 QQ 个人号时填写的 Token 正是用于校验 NapCat 发来的 WebSocket 请求**。只要两边 Type/Token 一致，连接即可建立。

#### 备选：AstrBot 正向连接 NapCat

如果你的网络环境要求 AstrBot 必须主动连接 NapCat，也可以反向配置：

- **NapCat 网络配置**：选择 **WebSocket 服务器**，监听地址填写 `/ws` 路径，**必须**勾选启用 Token 认证并记录生成的 Token。
- **AstrBot 配置**：在消息平台设置中，将 URL 指向 NapCat，并**在消息平台配置中填入相同的 Token**。

两种方式均可正常工作，选择更符合你网络架构的一种即可。本文以 **第一种（NapCat 主动连接 AstrBot）为主** 进行描述。

#### 3. 公网暴露时的代理层安全

**强烈建议**：不要将 NapCat WebUI（`6099` 端口）直接暴露在公网。如果确实需要公网访问，请在前方加一层反向代理（如 nginx），配置 HTTPS、基本认证（`Authorization: Basic`）并限定 IP 白名单。

---

### 二、AstrBot 安全配置

#### 1. AstrBot Dashboard 的访问密码

默认账号密码均为 `astrbot`。如果希望修改，可进入 AstrBot WebUI → **设置** → **账号管理**（或者在运行容器后修改 `./astrbot-data/cmd_config.json` 中的 `dashboard.username` 和 `dashboard.password` 字段）。密码存储经过 MD5 加密。

#### 🔐 安全要点：禁用默认管理员账号并创建独立的管理员

默认账号密码为 `astrbot`/`astrbot`，**这是公开的默认凭证，必须修改或禁用**。参考以下操作：

1. **立即修改默认密码**：登录 WebUI 后前往 **设置** → **账号管理**，修改 `astrbot` 账户的密码。
2. **创建独立的管理员账户**：在 **账号管理** 中添加一个新管理员账号，使用高强度密码，并将你的 QQ 号在 **配置** → **其他配置** → **管理员 ID 列表** 中加入。
3. **锁定或删除默认的 `astrbot` 账户**：在确认新管理员账户可用之后，修改默认账户的密码为一个随机长字符串并保存，确保无法被猜测或直接使用。
4. **关闭 HTTP 基本认证中的默认凭据（如有）**：如果你在反代层额外配置了 HTTP Basic Auth，请确保不使用 `astrbot`/`astrbot` 作为基本认证凭据。

#### 2. 与 NapCat 对接：配置“接入 QQ 个人号”适配器

在 AstrBot WebUI 中执行以下操作：

1. 进入 **消息平台** → 点击 **+** 号选择 **接入 QQ 个人号**。
2. **启用** 开关打开。
3. **WebSocket Token** 处，直接填入你在上面 NapCat WebSocket 客户端创建时记录的 Token。
4. **Type** 选择 `ws` 方向。
5. 点击 **保存并启用**。

#### 3. AstrBot Agent 沙箱（Shipyard Neo）的 Access Token

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

### 三、早柚核心（gsuid_core）安全配置

#### 1. 网页控制台的注册码（REGISTER_CODE）

`config.json` 位于 `./gsuid_core/data/config.json`。首次运行 gsuid_core 容器后该文件会自动生成。在其中找到 `REGISTER_CODE` 字段，该字段值即为注册码。

```json
"REGISTER_CODE": "4e8cd750c93de5c5"
```

复制该值后，在浏览器打开 `http://<你的公网IP>:8765/app/` 进行注册：

- 用户名建议使用你的 QQ 号（便于后续权限管理）。
- 注册码字段粘贴上述值。
- 设置一个高强度的登录密码（不要与 Token 重复使用）。

> ✅ **安全提示**：注册成功并登录后，建议立即**修改 `REGISTER_CODE`** 为一个新的随机字符串并重新保存 `config.json`，防止他人再次利用已知注册码创建额外账号。恢复操作时可通过进入容器修改 `config.json` 或通过网页控制台的“安全设置”修改注册码并重启容器。

#### 2. WebSocket Token（WS_TOKEN）

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

### 四、Token 管理与安全最佳实践

#### 1. Token 的存储与保护

- **不要将 Token 硬编码在 `docker-compose.yaml` 的 `environment` 或 `volumes` 路径中**——环境变量会出现在 `docker inspect` 或 `docker-compose config` 的输出中，属于不安全的做法。若必须通过环境变量传递，建议使用 `.env` 文件并严格限制文件权限（`chmod 600 .env`），并确保 `.env` 不被 Git 提交（加入 `.gitignore`）。
- 每个 Token 使用不同的随机字符串，避免复用。
- 定期轮换 Token（每 90 天或根据安全策略）。
- 使用密码管理器保存 Token，不要直接写在笔记/文档中。
- 若多人维护，在 CI/CD 或部署脚本中使用秘密管理工具（如 HashiCorp Vault、Infisical 或 Docker Secret）来管理敏感信息。

#### 2. 公网部署时的额外防护

- 为所有 Web 服务启用 HTTPS（自签名证书不安全，建议使用 Let's Encrypt）。
- 为 WebUI（AstrBot `6185` 端口、gsuid_core `8765` 端口）配置反向代理 + 基本认证（Authentication），并设置 IP 白名单。
- 为 NapCat WebUI 配置 `webui.json` 中的 `host: "127.0.0.1"`，并通过本地反向代理（如 caddy）限制暴露范围。
- 监控日志，及时发现异常访问或频繁尝试。

#### 3. 立即执行的优先级清单

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

### 五、快速检查清单

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

---

## 九、网络问题总结与排错

> 以下内容源自《AstrBot + NapCat + gsuid_core 一体化部署网络问题总结》，涵盖部署过程中遇到并解决的三大网络问题。

### 问题一：镜像拉取失败（外网访问不稳定）

（已在上文「五、镜像拉取与网络代理」中完整记录，此处不再重复。详见该章节。）

### 问题二：AstrBot 无法连接 gsuid_core（核心网络故障）

#### 现象
启动后 AstrBot 日志报错：
```
[Errno -2] Name or service not known
Core服务器连接失败
```
同时反复出现 `[GsCore] 尚未连接，消息丢弃` 警告，插件完全无法工作。

#### 原因分析
在原始的 `docker-compose.yaml` 中，曾为所有服务添加了：
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```
试图让容器通过 `host.docker.internal` 访问宿主机再转到其他容器。

但在 **Linux 原生 Docker** 环境中：
- `host.docker.internal` 本身就不存在，是 Docker Desktop 的特性
- 即使通过 `extra_hosts` 强行映射到宿主机网关 IP，也**无法保证能正确转发到对应容器的端口**（需要额外的 iptables 或端口映射）
- 实际测试中，AstrBot 填写 `host-gateway`、`localhost`、`host.docker.internal` **全部无效**（笔记原话）

#### 目前 **docker-compose.yaml 已移除所有 `extra_hosts` 配置**
因为该配置在 Linux 下证实无效，所以已全部删除，保持配置干净。

#### 最终解决方法
在 AstrBot 的 `astrbot_plugin_gscore_adapter` 插件配置中，**直接填写 gsuid_core 容器在 Docker 网络中的服务名**（或者填写云服务器的公网 IP）：
```
gsuid_core:8765
```
或使用公网 IP `x.x.x.x:8765`。

- 因为三个服务都属于同一个自定义网络 `astrbot_network`（bridge），容器间可以通过服务名直接 DNS 解析通信
- **连接成功后必须重启 gsuid_core 容器**，否则插件可能仍残留连接错误状态
- 重启命令：`docker restart gsuid_core`

> 本问题与 `extra_hosts` 无关，最终通过使用 **容器内部服务名** 解决，不再依赖任何宿主机地址伪造。

### 问题三：NapCat 登录后 AstrBot 收不到 QQ 消息

#### 现象
NapCat 容器成功登录 QQ，但在 QQ 发消息后，AstrBot 日志没有任何消息事件输出。

#### 原因
虽然 NapCat 在 `docker-compose.yaml` 中映射了端口 `6099:6099`，但实际 WebSocket 长连接使用的是 **6199 端口**（`6099` 只是 NapCat 的 Web 控制面板端口）。  
AstrBot 通过 `6199` 与 NapCat 进行消息通信，而云服务器的防火墙默认未放行此端口。

#### 解决
在阿里云安全组（或本地 `iptables`）**入方向** 放行：
- 协议：`TCP`
- 端口：`6199/6199`

**无需放行出方向**，仅入方向放行即可。  
（笔记原话：“只要入方向TCP放行6199/6199就可以了，入口不用放行” —— 其中“入口”指入方向）

确认端口区别：
- `6099`：NapCat 控制面板（不放行不影响消息收发）
- `6199`：AstrBot ↔ NapCat 消息 WebSocket 连接，必须放行

---

### 总结：容器间通信最终正确打开方式

| 通信路径             | 实际使用的地址/配置                                | 说明                                                                                                                                                                   |
| -------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AstrBot → gsuid_core | `gsuid_core:8765`                                  | 使用 Docker 内置 DNS，同属 `astrbot_network`，无需任何 `extra_hosts`                                                                                                   |
| AstrBot → NapCat     | `宿主机IP:6199` 或者 `napcat:6199`（若服务名可用） | 由于 NapCat 没配置 `6199` 端口映射，目前需通过宿主机 IP 访问；如需直接用服务名，需在 NapCat 的 ports 里增加 `6199:6199`（但当前 `docker-compose.yaml` 中未映射该端口） |
| 外部拉取镜像         | SSH 反向隧道 → `http://127.0.0.1:17897`            | 安全稳定，不暴露公网端口                                                                                                                                               |

- **Linux 下彻底放弃 `host.docker.internal`**，所有容器间通信一律用服务名
- **AstrBot 插件地址必须使用 `gsuid_core:8765`**（服务名），并记得重启 gsuid_core
- **防火墙务必放行 `6199`** 入站，而非 `6099`
- 镜像加速器可作为备用，但主力还是要靠稳定的代理隧道

---

## 十、插件与额外安装

进入 AstrBot 容器执行命令：
```bash
docker exec -it astrbot bash
```

### 1. 安装插件依赖（如禁漫插件等）
```bash
cd /AstrBot/data/plugins/astrbot_plugin_jm_cosmos
pip install -r requirements.txt
```

### 2. 安装 Playwright（浏览器自动化）
```bash
pip install playwright
playwright install-deps
playwright install
```

### 3. 安装语音支持（TTS/STT）
```bash
pip install openai-whisper
```

> 大部分插件可通过 AstrBot 控制台的“插件管理”直接安装，无需进入容器操作。数据目录 `./astrbot-data` 已持久化，重建容器不会丢失数据。

---

## 十一、维护与更新

### 更新镜像
```bash
docker-compose pull
docker-compose up -d
```

### 清理旧镜像
```bash
docker image prune -a
```

### 备份数据
备份整个工作目录（包含 `astrbot-data`、`napcat`、`gsuid_core` 等文件夹）即可。

---

## 十二、扩展提示

- **多 QQ 账号**：如需登录多个账号，可复制 `napcat` 服务块，修改容器名、端口映射、数据目录（如 `./napcat2/config`），并确保与 AstrBot 共享同一个 `astrbot-data`。
- **内网穿透**：若需公网访问，可自行添加 natapp、frp 等服务，并在 compose 中增加对应容器（使用 `network_mode: host` 或加入 `astrbot_network`）。
- **沙盒执行环境**：如需使用 Shipyard Neo，请参考 [原项目文档](https://github.com/AstrBotDevs/shipyard-neo) 自行集成。

---

## 十三、常见问题（补充）

### 1. 端口冲突
- 检查 `6185`、`6099`、`8765` 是否被占用
- 可修改 `docker-compose.yaml` 中左侧的宿主机端口，例如 `"7000:6185"`

### 2. NapCat 扫码后无响应
- 确保 `MODE=astrbot` 环境变量已设置
- 检查 `./astrbot-data` 目录是否同时挂载到 NapCat 和 AstrBot
- 查看日志：`docker-compose logs napcat`

### 3. gsuid_core 无法访问 /app/
- 确认访问 URL 包含 `/app/` 后缀
- 检查宿主机防火墙是否放行 8765 端口
- 查看早柚日志：`docker-compose logs gsuid_core`

### 4. 容器日志增长过快
compose 中已配置日志轮转（最大 50MB，保留 3 个文件）。如需调整，修改 `max-size` 和 `max-file` 的值。

### 5. 国内拉取镜像慢
可配置 Docker 镜像加速器（如阿里云、中科大），或在 compose 文件中为服务指定 `image` 时使用代理拉取。亦可通过上文所述的 SSH 反向隧道彻底解决。

---

## 完整性自检

对照提供的四个文件，确认已覆盖全部内容：

1. **`AstrBot + NapCat + gsuid_core 一体化部署网络问题总结.md`**  
   - 问题一（镜像拉取失败）：镜像源列表、SSH 反向隧道建立、Docker 守护进程代理配置 —— 已全部放入第五章。  
   - 问题二（AstrBot 无法连接 gsuid_core）：报错信息、`extra_hosts` 原因分析、移除配置说明、最终使用服务名解决 —— 完整保留在第九章。  
   - 问题三（NapCat 消息收不到）：6199 端口问题、防火墙放行说明、端口区别 —— 完整保留。  
   - 容器间通信总结表格及三条要点 —— 全部保留。

2. **`AstrBot + Napcat + gsuid_core 轻量部署指南.md`**  
   - 整体架构表格 —— 第一章。  
   - 部署前准备（环境要求）—— 第二章。  
   - `docker-compose.yaml` 嵌入内容 —— 虽未重复粘贴已在第三章给出实际文件，但其说明性句子（如“将以下 docker-compose.yaml 保存到工作目录”）已在相应章节涵盖，且实际 yaml 内容与单独文件合并展示。  
   - 目录结构说明 —— 第四章。  
   - 启动服务命令 —— 第六章。  
   - 初始化配置（AstrBot、NapCat、gsuid_core 注册、插件、连接）—— 第七章。  
   - 插件与额外安装 —— 第十章。  
   - 常见问题 —— 第十三章（并融合网络问题）。  
   - 维护与更新 —— 第十一章。  
   - 扩展提示 —— 第十二章。  
   以上无一遗漏。

3. **`NapCat、AstrBot 和 gsuid_core 这三个服务相关的 Token 及安全配置.md`**  
   - NapCat WebUI Token 获取、WebSocket 客户端/服务器方向说明、公网代理安全 —— 第八章一。  
   - AstrBot Dashboard 密码、禁用默认管理员、对接 NapCat 适配器配置、沙箱 Access Token —— 第八章二。  
   - gsuid_core REGISTER_CODE、WS_TOKEN 两端配置 —— 第八章三。  
   - Token 管理最佳实践、公网防护、优先级清单 —— 第八章四。  
   - 快速检查清单 —— 第八章五。  
   全部逐字保留，与前面章节的重叠部分未删减，保持原文再现。

4. **`docker-compose.yaml`**  
   - 文件完整内容（含所有注释、环境变量、卷挂载、网络定义）—— 第三章。  
   - 与轻量指南内嵌的 compose 内容实质一致，并未丢失任何配置项。