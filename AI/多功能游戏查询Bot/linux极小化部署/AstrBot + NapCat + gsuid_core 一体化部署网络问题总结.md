# AstrBot + NapCat + gsuid_core 一体化部署网络问题总结

> **部署目录**：`/opt/bot/`，该目录下存放 `docker-compose.yaml`  
> **启动命令**：`docker compose up -d`（在 `/opt/bot/` 内执行）  
> **当前状态**：`extra_hosts` 已从所有服务中移除，因为实践证明在 Linux 下该配置无效。

---

## 问题一：镜像拉取失败（外网访问不稳定）

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

## 问题二：AstrBot 无法连接 gsuid_core（核心网络故障）

### 现象
启动后 AstrBot 日志报错：
```
[Errno -2] Name or service not known
Core服务器连接失败
```
同时反复出现 `[GsCore] 尚未连接，消息丢弃` 警告，插件完全无法工作。

### 原因分析
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

### 目前 **docker-compose.yaml 已移除所有 `extra_hosts` 配置**
因为该配置在 Linux 下证实无效，所以已全部删除，保持配置干净。

### 最终解决方法
在 AstrBot 的 `astrbot_plugin_gscore_adapter` 插件配置中，**直接填写 gsuid_core 容器在 Docker 网络中的服务名**（或者填写云服务器的公网 IP）：
```
gsuid_core:8765
```
或使用公网 IP `x.x.x.x:8765`。

- 因为三个服务都属于同一个自定义网络 `astrbot_network`（bridge），容器间可以通过服务名直接 DNS 解析通信
- **连接成功后必须重启 gsuid_core 容器**，否则插件可能仍残留连接错误状态
- 重启命令：`docker restart gsuid_core`

> 本问题与 `extra_hosts` 无关，最终通过使用 **容器内部服务名** 解决，不再依赖任何宿主机地址伪造。

---

## 问题三：NapCat 登录后 AstrBot 收不到 QQ 消息

### 现象
NapCat 容器成功登录 QQ，但在 QQ 发消息后，AstrBot 日志没有任何消息事件输出。

### 原因
虽然 NapCat 在 `docker-compose.yaml` 中映射了端口 `6099:6099`，但实际 WebSocket 长连接使用的是 **6199 端口**（`6099` 只是 NapCat 的 Web 控制面板端口）。  
AstrBot 通过 `6199` 与 NapCat 进行消息通信，而云服务器的防火墙默认未放行此端口。

### 解决
在阿里云安全组（或本地 `iptables`）**入方向** 放行：
- 协议：`TCP`
- 端口：`6199/6199`

**无需放行出方向**，仅入方向放行即可。  
（笔记原话：“只要入方向TCP放行6199/6199就可以了，入口不用放行” —— 其中“入口”指入方向）

确认端口区别：
- `6099`：NapCat 控制面板（不放行不影响消息收发）
- `6199`：AstrBot ↔ NapCat 消息 WebSocket 连接，必须放行

---

## 总结：容器间通信最终正确打开方式

| 通信路径             | 实际使用的地址/配置                                | 说明                                                                                                                                                                   |
| -------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AstrBot → gsuid_core | `gsuid_core:8765`                                  | 使用 Docker 内置 DNS，同属 `astrbot_network`，无需任何 `extra_hosts`                                                                                                   |
| AstrBot → NapCat     | `宿主机IP:6199` 或者 `napcat:6199`（若服务名可用） | 由于 NapCat 没配置 `6199` 端口映射，目前需通过宿主机 IP 访问；如需直接用服务名，需在 NapCat 的 ports 里增加 `6199:6199`（但当前 `docker-compose.yaml` 中未映射该端口） |
| 外部拉取镜像         | SSH 反向隧道 → `http://127.0.0.1:17897`            | 安全稳定，不暴露公网端口                                                                                                                                               |

- **Linux 下彻底放弃 `host.docker.internal`**，所有容器间通信一律用服务名
- **AstrBot 插件地址必须使用 `gsuid_core:8765`**（服务名），并记得重启 gsuid_core
- **防火墙务必放行 `6199`** 入站，而非 `6099`
- 镜像加速器可作为备用，但主力还是要靠稳定的代理隧道

以上记录基于实际踩坑过程，保留了全部笔记细节，文件路径 `/opt/bot/docker-compose.yaml` 对应的修改均已体现。