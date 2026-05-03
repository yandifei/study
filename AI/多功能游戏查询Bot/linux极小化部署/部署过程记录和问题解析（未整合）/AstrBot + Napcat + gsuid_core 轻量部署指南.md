# 基于 docker-compose 的 AstrBot + NapCat + gsuid_core 部署指南

本指南基于提供的 `docker-compose.yaml` 编写，仅包含实际部署的服务：**AstrBot**（机器人主框架）、**NapCat**（QQ 协议客户端）、**gsuid_core**（早柚核心，游戏助手后端）。不包含 Shipyard Neo、Bay、natapp 等未在 compose 文件中定义的服务。

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

### 2. 准备文件
将以下 `docker-compose.yaml` 保存到工作目录（例如 `~/qqbot/`）：

```yaml
# AstrBot + Napcat + gsuid_core 一体化部署
services:
  astrbot:
    image: soulter/astrbot:latest
    container_name: astrbot
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
    ports:
      - "${ASTRBOT_PORT:-6185}:6185"
      - "4141:4141"
    volumes:
      - ./astrbot-data:/AstrBot/data
    networks:
      - astrbot_network
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"

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
      - ./astrbot-data:/AstrBot/data
      - ./napcat/config:/app/napcat/config
      - ./napcat/ntqq:/app/.config/QQ
    networks:
      - astrbot_network

  gsuid_core:
    image: docker.cnb.cool/gscore-mirror/gsuid_core:latest
    container_name: gsuid_core
    ports:
      - "8765:8765"
    volumes:
      - ./gsuid_core/data:/gsuid_core/data
      - ./gsuid_core/plugins:/gsuid_core/gsuid_core/plugins
      - venv-data:/venv
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
      - UV_INDEX=https://pypi.org/simple/
      - UV_NO_CONFIG=0
      - no_proxy="localhost,127.0.0.1,.local,cnb.cool,mirrors.aliyun.com,pypi.tuna.tsinghua.edu.cn,mirrors.volces.com"
    networks:
      - astrbot_network

networks:
  astrbot_network:
    name: astrbot_network
    driver: bridge

volumes:
  venv-data:
```

---

## 三、目录结构说明

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

## 四、启动服务

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

## 五、初始化配置

### 1. 配置 AstrBot

访问 WebUI：`http://<宿主机IP>:6185`  
默认账号：`astrbot`  
默认密码：`astrbot`

登录后建议立即修改密码（右上角个人设置）。

#### （可选）配置 AI 服务
AstrBot 本身不强制依赖外部 AI，若要使用 ChatGPT 等，请进入 **AI 配置** 填写相应的 API Key 和端点。

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

---

## 六、插件与额外安装

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

## 七、常见问题

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
可配置 Docker 镜像加速器（如阿里云、中科大），或在 compose 文件中为服务指定 `image` 时使用代理拉取。

---

## 八、维护与更新

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

## 九、扩展提示

- **多 QQ 账号**：如需登录多个账号，可复制 `napcat` 服务块，修改容器名、端口映射、数据目录（如 `./napcat2/config`），并确保与 AstrBot 共享同一个 `astrbot-data`。
- **内网穿透**：若需公网访问，可自行添加 natapp、frp 等服务，并在 compose 中增加对应容器（使用 `network_mode: host` 或加入 `astrbot_network`）。
- **沙盒执行环境**：如需使用 Shipyard Neo，请参考 [原项目文档](https://github.com/AstrBotDevs/shipyard-neo) 自行集成。

---

按照本指南操作，你将拥有一个完整的 QQ 机器人 + 游戏助手系统，所有服务通过 Docker 统一管理，数据持久化且易于备份迁移。