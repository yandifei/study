# AstrBot + Napcat + Shipyard Neo + gsuid_core + natapp 一体化部署指南

本文档整合了所有相关服务的部署步骤、配置说明以及常见问题处理，基于一套 `docker-compose.yaml` 实现全量部署。适合希望快速搭建多账号 QQ 机器人 + 沙盒执行环境 + 原神/鸣潮等游戏助手的用户。

---

## 一、整体架构

| 服务           | 用途                           | 端口映射 (宿主机:容器)   | 备注                    |
| -------------- | ------------------------------ | ------------------------ | ----------------------- |
| **astrbot**    | 机器人主框架 (WebUI + API)     | `6185:6185`、`4141:4141` | 依赖 bay 健康检查       |
| **napcat1**    | QQ 协议客户端 1 (MODE=astrbot) | `6099:6099`              | 与 astrbot 共享数据目录 |
| **napcat2**    | QQ 协议客户端 2                | `6100:6099`              | 使用不同配置目录        |
| **bay**        | Shipyard Neo 沙盒管理 API      | `8114:8114`              | 需挂载 docker.sock      |
| **gsuid_core** | 早柚核心 (原神等游戏 bot 后端) | `8765:8765`              | 需要配合框架插件使用    |
| **natapp**     | 内网穿透 (可选)                | 使用 host 网络           | 需要配置 authtoken      |

---

## 二、部署前准备

### 1. 环境要求
- 已安装 Docker 和 Docker Compose (v2 推荐)
- 操作系统：Linux (推荐) / Windows (需支持 Docker)
- 至少 4GB 可用内存，10GB 磁盘空间

### 2. 获取核心配置文件
项目仓库：`https://github.com/AstrBotDevs/shipyard-neo`  
我们只需要部署目录下的 Compose 文件和 Bay 配置，不参与源码构建。推荐使用稀疏检出节省空间：

```bash
git clone --filter=blob:none --no-checkout https://github.com/AstrBotDevs/shipyard-neo
cd shipyard-neo
git sparse-checkout set deploy/docker pkgs/bay pkgs/gull pkgs/ship
git checkout
cd deploy/docker
```

或者直接下载压缩包，仅提取以下两个核心文件：
- `docker-compose.yaml` (本指南提供的一体化文件)
- `config.yaml` (Bay 的配置文件)

**本文提供的 `docker-compose.yaml` 已整合 AstrBot、Napcat (双实例)、Bay、gsuid_core、natapp，无需再组合多个 Compose 文件。**

---

## 三、配置文件详解

### 1. `docker-compose.yaml` 关键点

完整内容见附件（开头给出的文件）。注意事项：

- **网络**：所有服务加入自定义网络 `astrbot_network`，保证容器间直接通信。
- **AstrBot**：
  - 通过 `BAY_DATA_DIR=/bay-data` 和卷挂载 `./bay-data:/bay-data:ro` 自动发现 Bay 的 API 密钥。
  - 健康检查依赖 `bay` 服务。
- **Napcat 实例**：
  - `napcat1` 使用宿主端口 `6099`，配置目录 `./napcat1/`
  - `napcat2` 使用宿主端口 `6100`，配置目录 `./napcat2/`
  - 两个实例均挂载 `./astrbot-data:/AstrBot/data`，使得 AstrBot 能管理多个 QQ 账号。
  - 环境变量 `MODE=astrbot` 表示以 AstrBot 模式运行。
- **Bay**：
  - 挂载 `docker.sock` 用于动态创建沙盒容器。
  - 挂载 `./config.yaml` 配置文件（只读）。
  - 数据目录 `./bay-data` 持久化 SQLite 数据库及自动生成的 `credentials.json`。
- **gsuid_core**：
  - 挂载 `./gsuid_core/data`、`./gsuid_core/plugins`、独立卷 `venv-data` 保存 Python 虚拟环境。
  - `extra_hosts` 使容器内可通过 `host.docker.internal` 访问宿主机。
  - 可配置 PyPI 镜像源和代理（根据网络情况调整）。
- **natapp**：
  - 使用 `network_mode: "host"` 直接共享宿主机网络。
  - 环境变量 `authtoken` 需替换为实际隧道令牌。
- **卷/日志限制**：大部分服务配置了日志轮转，防止磁盘写满。

### 2. `config.yaml` (Bay 配置) 必须修改项

**API Key**：必须设置为一个强随机字符串。

```bash
# 宿主机执行，生成随机密钥
openssl rand -hex 32
```

将输出结果替换到 `config.yaml` 中的 `security.api_key` 字段。

```yaml
security:
  api_key: "你生成的随机字符串"   # 此处替换
  allow_anonymous: false
```

其他重要参数（通常无需修改）：
- `driver.docker.network: "astrbot_network"` 必须与 Compose 中的网络名称一致。
- `cargo.root_path: "/workspace"` 与 Compose 中 Bay 卷挂载对应。
- `proxy` 部分根据实际代理需求调整，如果不用代理可将 `enabled: false`。

**注意**：一旦设置了固定的 `api_key`，AstrBot 的 Access Token 就不能留空，必须手动填入此密钥（详见第四部分第3节）。

---

## 四、启动与初始化

### 1. 启动所有服务

将所有文件（`docker-compose.yaml`、`config.yaml`）放在同一目录，执行：

```bash
docker-compose up -d
```

首次启动会自动拉取镜像，稍等片刻。使用 `docker-compose ps` 确认所有容器状态为 `Up` 或 `healthy`。

### 2. 可选：清理无效网络/镜像

```bash
docker network prune -f
docker image prune
```

### 3. 配置 AstrBot 与 Shipyard Neo

访问 AstrBot 控制台：`http://<宿主机IP>:6185`  
默认账号：`astrbot`  
默认密码：`astrbot`

登录后进入 **AI 配置 → Agent Computer Use**，进行如下配置：

| 设置项               | 值                                                                                                                                              | 说明                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| Computer Use Runtime | `sandbox`                                                                                                                                       | 使用沙盒模式               |
| 沙箱环境驱动器       | `shipyard_neo`                                                                                                                                  | 选择 Shipyard Neo 驱动     |
| Endpoint             | `http://bay:8114`                                                                                                                               | Bay 在 Docker 网络内的 DNS |
| Access Token         | **若已在 config.yaml 设置了固定 key**：填入与 `security.api_key` 完全相同的值；**若未设置固定 key**：留空，AstrBot 会自动从 `bay-data` 卷中读取 | 根据实际情况选择           |

点击“保存”，若看到“保存成功~”且无警告，则配置正确。

### 4. NapCat 登录

两个 Napcat 实例分别通过各自端口暴露 WebUI 或使用手机 QQ 扫码登录。具体操作需根据 Napcat 官方文档完成。  
配置文件在 `./napcat1/config/` 和 `./napcat2/config/`，可按需修改 OneBot 相关设置。

### 5. 早柚核心 (gsuid_core) 配置

#### 访问控制台
- 地址：`http://<宿主机IP>:8765/app/`
- 注意：不带 `/app/` 无法进入管理界面。

#### 创建账号
首次使用需要注册账号：
- 点击登录页面的注册，输入你的 QQ 号作为账号，设置密码。
- 注册码（REGISTER_CODE）在 `./gsuid_core/data/config.json` 中的 `REGISTER_CODE` 字段，每个人的随机码不同。

#### 安全设置（可选，生产推荐）
编辑 `./gsuid_core/data/config.json`，找到 `WS_TOKEN` 并设置一个强随机字符串。  
然后进入 AstrBot 的插件 `astrbot_plugin_gscore_adapter` 配置，将 `WS_TOKEN` 填为相同的值；同时将请求地址中的 `localhost` 改为 `host.docker.internal`，因为核心和框架都在 Docker 但跨容器通信。

插件配置示例：
```
ws://host.docker.internal:8765
```

#### 安装早柚插件
在早柚控制台 → 插件管理 中，可安装各类游戏插件，例如：
- 原神：`GenshinUID`
- 鸣潮：`XutheringWavesUID`
更全列表参考 [早柚文档](https://docs.sayu-bot.com/InstallPlugins/PluginsList.html)

### 6. Natapp 隧道配置

修改 `docker-compose.yaml` 中 natapp 服务的环境变量：
```yaml
environment:
  - authtoken=<你的隧道authtoken>
```
若需要详细日志，取消 `loglevel=DEBUG` 注释。

---

## 五、插件与额外环境安装

进入 AstrBot 容器执行命令：

```bash
docker exec -it astrbot bash
```

### 1. 禁漫插件 (astrbot_plugin_jm_cosmos)
依赖需手动安装：
```bash
cd /AstrBot/data/plugins/astrbot_plugin_jm_cosmos
pip install -r requirements.txt
```

### 2. Playwright (浏览器自动化)
```bash
pip install playwright
playwright install-deps
playwright install
```

### 3. 语音相关（TTS/STT）
```bash
pip install openai-whisper
```

### 4. 插件市场安装其他插件
在 AstrBot 控制台 → 插件管理 中直接搜索安装，大多数插件不需要手动进容器。

**注意**：AstrBot 数据目录 `./astrbot-data` 持久化了所有插件和数据，重建容器不会丢失。

---

## 六、常见问题

1. **端口冲突**  
   检查 `6185`、`6099`、`6100`、`8114`、`8765` 等端口是否被占用，必要可在 `docker-compose.yaml` 中调整映射。

2. **Bay 健康检查失败**  
   确认 `config.yaml` 中 `driver.docker.network` 为 `astrbot_network`；确认 docker.sock 挂载正确。

3. **AstrBot 无法连接沙盒**  
   检查 Endpoint 是否填写 `http://bay:8114`，若设置了固定 API Key 则 Access Token 必须完全一致。

4. **gsuid_core 无法连接**  
   检查宿主机防火墙是否放行 8765 端口；若从 AstrBot 插件连接，确保地址使用 `host.docker.internal` 而非 `localhost`。

5. **NapCat 扫码后无响应**  
   检查 `MODE=astrbot` 是否设置，数据卷挂载是否正确，网络是否同在 `astrbot_network`。

6. **容器日志无限增长**  
   已在 Compose 文件中配置 `max-size` 和 `max-file`，可自行调整参数。

---

## 七、维护与更新

- **更新镜像**：`docker-compose pull` 然后 `docker-compose up -d`。
- **清理旧镜像**：`docker image prune -a`。
- **备份数据**：整个工作目录（包含 `astrbot-data`、`bay-data`、`gsuid_core`、`napcat1`、`napcat2` 等文件夹）即可。

---

至此，你的多账户 QQ 机器人、沙盒 Python 执行器、游戏助手核心和可选内网穿透已全部在 Docker 中统一运行。如需扩展其他服务，只需修改 `docker-compose.yaml` 后再次执行 `docker-compose up -d`。