# Docker 代理配置完整指南（Windows 代理借给 Linux 服务器）

## 背景与需求

- 你在 **Windows 11** 上运行 Verge Clash 代理（混合端口 `127.0.0.1:7897`）
- 希望让 **阿里云 Linux 服务器** 通过该代理访问外网（尤其是拉取 Docker 镜像）
- 核心障碍：
  - 内网穿透：服务器无法直接访问你 Windows 的内网 IP
  - Docker 不读取 Shell 环境变量，需要单独为 Docker 守护进程配置代理

## 整体解决方案

**SSH 反向隧道 + 为 Docker 守护进程配置代理**  
无需开放公网端口，安全稳定。

---

## 第一步：在 Windows 上建立 SSH 反向隧道

在 Windows 的 CMD、PowerShell 或 Tabby 终端中执行（保持窗口运行）：

```bash
ssh -R 17897:127.0.0.1:7897 root@你的阿里云服务器IP
```

- `-R`：远程转发（Remote）
- `17897`：阿里云服务器上监听的本地端口（可自定义，**无需在安全组放行**）
- `127.0.0.1:7897`：你 Windows 上 Verge Clash 的混合端口（需开启 Allow LAN）

> 隧道建立后，服务器上访问 `127.0.0.1:17897` 就等同于访问你 Windows 的 `127.0.0.1:7897`。

---

## 第二步：为 Docker 守护进程配置代理

SSH 登录到阿里云服务器，执行以下命令：

```bash
# 1. 创建 systemd drop-in 目录
sudo mkdir -p /etc/systemd/system/docker.service.d

# 2. 写入代理配置文件
sudo tee /etc/systemd/system/docker.service.d/proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:17897"
Environment="HTTPS_PROXY=http://127.0.0.1:17897"
Environment="NO_PROXY=localhost,127.0.0.1,.local"
EOF

# 3. 重载配置并重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# 4. 验证代理已生效（应输出刚设置的环境变量）
sudo systemctl show --property=Environment docker
```

之后执行 `docker pull` 或 `docker compose up -d` 即可通过代理拉取镜像。

---

## 常见问题及解决方法

### 问题一：卡在 Vim 编辑界面，不知道如何保存退出

- **现象**：打开文件后停留在 Vim，无法退出。
- **解决**：
  1. 按 `Esc` 进入普通模式
  2. 输入 `:` 进入命令模式
  3. 输入 `wq` 回车 → 保存并退出  
     或 `:q!` → 不保存强制退出

### 问题二：保存时提示 `E45: 'readonly' option is set`

- **现象**：没有用 `sudo` 打开系统文件，导致只读。
- **解决**：
  - **提权保存（推荐）**：`:w !sudo tee %` → 输入 sudo 密码 → `:q` 退出
  - **放弃保存**：`:q!`
- **预防**：始终使用 `sudo vim 文件名` 打开 `/etc/` 下的文件。

### 问题三：打开文件时遇到 `E325: ATTENTION` – 发现交换文件（.swp）

- **现象**：提示存在上次异常退出的 `.swp` 文件。
- **解决**：
  1. 按空格键（或回车）滚动完提示消息，出现选项菜单
  2. 按 `D` 删除旧的 swap 文件，然后正常编辑保存  
     或者退出后手动删除：`sudo rm /etc/systemd/system/docker.service.d/.proxy.conf.swp`

---

## 可选辅助方案：配置国内镜像加速器

如果 SSH 隧道在大流量下不稳定（如出现 `tls: bad record MAC`），可添加国内镜像源作为备用：

```bash
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF
sudo systemctl restart docker
```

---

## 需要避免的错误做法

| 错误做法                                      | 后果                                                               |
| --------------------------------------------- | ------------------------------------------------------------------ |
| 在阿里云安全组放行 Clash 端口（如 7897）      | 任何人都能把你 Windows 当公开代理，流量耗尽、节点被封、法律风险    |
| 在阿里云安全组放行反向隧道端口（如 17897）    | 没必要（该端口只监听 127.0.0.1），放行无意义，还可能误以为需要开放 |
| 只设置 Shell 环境变量 `export http_proxy=...` | 对 Docker 守护进程无效，导致镜像拉取失败                           |
| 试图配置“Linux 全局代理”                      | 复杂且易破坏 SSH 连接本身，不建议                                  |
| 在 Tabby 里混淆“本地/远程”转发方向            | 隧道无法建立，出现 `Connection refused` 或 `ChannelOpenFailure`    |

---

## 总结

- **最安全、最简洁的“借用”方法**：SSH 反向隧道，无需任何额外工具或公网端口。
- **让 Docker 使用代理的正确姿势**：配置 systemd drop-in 文件为 Docker 守护进程设置 `HTTP_PROXY`。
- **网络不稳定时的补充**：同时配置国内镜像加速器，避免隧道下载失败。

按照以上步骤操作后，你的阿里云服务器即可通过 Windows 上的 Verge Clash 代理稳定拉取 Docker 镜像。