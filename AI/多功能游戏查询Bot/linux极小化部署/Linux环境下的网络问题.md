## 问题原因

在 **Linux 宿主环境** 下，Docker 容器内默认**无法解析** `host.docker.internal` 这个特殊域名（该域名仅存在于 Docker Desktop for Mac/Windows）。

虽然 `gsuid_core` 容器通过监听 `0.0.0.0:8765` 提供服务，且已经在 `docker-compose.yml` 中为它添加了 `extra_hosts`，但 **`astrbot` 容器并未配置该映射**，导致它尝试连接 `ws://host.docker.internal:8765/...` 时出现 `Name or service not known` 错误。

---

## 解决方案

为 `astrbot` 服务也添加 `extra_hosts` 配置，将 `host.docker.internal` 映射到 `host-gateway`（即宿主机的可访问网关地址）。

```yaml
services:
  astrbot:
    # ... 原有配置 ...
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

然后通过以下命令重新创建容器使配置生效：

```bash
docker compose up -d --force-recreate astrbot
```

---

## 关键要点

1. **`host.docker.internal` 并非 Linux Docker 原生支持**，需要手动通过 `extra_hosts` 定义。
2. **同一 Compose 网络中的容器**也可以通过**服务名**互相访问（如 `gsuid_core`），但插件配置中若固定使用了 `host.docker.internal`，则必须为该容器添加这条 `extra_hosts` 记录。
3. `extra_hosts: - "host.docker.internal:host-gateway"` 是 Linux 下实现类似 Docker Desktop 域名解析的通用做法。

调整后，`AstrBot` 能够正确解析地址并连上 `gsuid_core` 的 WebSocket 服务，消息不再丢失。****