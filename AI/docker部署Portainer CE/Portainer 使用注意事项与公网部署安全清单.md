# Portainer 使用注意事项与公网部署安全清单

## 1. 总原则

Portainer 是 Docker 的可视化管理面板，拥有很高权限。

如果 Portainer 能控制 Docker，那么它就可以：

* 创建容器
* 删除容器
* 挂载宿主机目录
* 读取容器日志
* 修改部署配置
* 操作镜像、网络、数据卷
* 间接影响宿主机安全

因此，Portainer 一旦暴露到公网，就必须当成一个高权限管理入口来保护。

一句话原则：

```text
Portainer 可以公网访问，但不能裸奔。
```

---

## 2. 不建议开放 9000 端口

如果要公网访问，建议使用：

```text
9443
```

访问方式：

```text
https://你的公网IP:9443
```

不建议公网开放：

```text
9000
```

原因：

* `9000` 通常是 HTTP
* 明文 HTTP 不适合公网管理后台
* 登录凭据和管理操作应尽量走 HTTPS
* 现代 Portainer 默认更推荐使用 `9443`

推荐 Compose 配置：

```yaml
services:
  portainer:
    image: portainer/portainer-ce:lts
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9443:9443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./portainer_data:/data
```

---

## 3. Docker Socket 风险

Portainer 通常会挂载：

```yaml
- /var/run/docker.sock:/var/run/docker.sock
```

这个配置是 Portainer 能管理 Docker 的关键。

但它也意味着 Portainer 拥有非常高的权限。

如果攻击者登录了你的 Portainer，基本就可以控制你的 Docker 环境，甚至可能进一步影响宿主机。

所以必须注意：

* 不要使用弱密码
* 不要随便创建管理员账号
* 不要把 Portainer 暴露给所有人
* 不要在 Portainer 中运行来历不明的 Compose
* 不要随意给容器挂载宿主机敏感目录

尤其要避免这类危险挂载：

```yaml
volumes:
  - /:/host
```

或者：

```yaml
volumes:
  - /etc:/etc
  - /root:/root
  - /var/run/docker.sock:/var/run/docker.sock
```

除非你非常清楚自己在做什么。

---

## 4. 管理员账号安全

首次初始化 Portainer 时，建议：

* 不要使用 `admin` 作为用户名
* 不要使用简单密码
* 密码至少 16 位
* 使用大小写字母、数字、符号组合
* 不要与其他网站重复使用同一个密码
* 保存到密码管理器

不推荐密码：

```text
admin123
password
12345678
portainer123
你的手机号
你的生日
```

推荐密码形式：

```text
随机生成的 16-32 位复杂密码
```

---

## 5. 公网访问建议

如果必须公网访问，建议优先级如下：

### 方案一：VPN 访问

最安全推荐：

```text
公网不直接开放 Portainer
通过 VPN 进入内网后再访问
```

可选工具：

* WireGuard
* Tailscale
* ZeroTier
* OpenVPN

例如只允许通过 VPN 访问：

```text
https://内网IP:9443
```

---

### 方案二：限制来源 IP

如果你有固定公网 IP，可以在防火墙中只允许自己的 IP 访问。

例如使用 UFW：

```bash
sudo ufw allow from 你的固定公网IP to any port 9443 proto tcp
sudo ufw deny 9443/tcp
```

查看规则：

```bash
sudo ufw status
```

---

### 方案三：反向代理 + 域名 + 正式 HTTPS

如果你有域名，可以使用：

* Nginx
* Caddy
* Traefik
* Nginx Proxy Manager

示例访问方式：

```text
https://portainer.example.com
```

反向代理适合配合：

* 正式 HTTPS 证书
* 访问日志
* IP 白名单
* Basic Auth
* WAF
* 统一入口管理

---

### 方案四：直接开放 9443

这是最简单的方式，但安全性最低。

适合临时使用或个人低风险环境。

最低要求：

* 只开放 `9443`
* 不开放 `9000`
* 使用强密码
* 及时更新系统和 Portainer
* 不要在 Portainer 里运行陌生模板
* 开启云服务器安全组限制
* 开启系统防火墙

---

## 6. 云服务器安全组设置

如果服务器在云厂商上，例如：

* 阿里云
* 腾讯云
* 华为云
* AWS
* Azure
* Vultr
* Hetzner
* Oracle Cloud

需要同时检查：

1. 云服务器安全组
2. 系统防火墙
3. Docker 端口映射
4. 反向代理配置

即使系统防火墙关闭了，云安全组开放也可能暴露服务。

建议只开放必要端口：

```text
22    SSH，建议限制 IP 或改用密钥
80    HTTP，只有反向代理需要
443   HTTPS，只有反向代理需要
9443  Portainer，建议限制 IP
```

不建议随便开放：

```text
3306  MySQL
5432  PostgreSQL
6379  Redis
27017 MongoDB
9000  Portainer HTTP
2375  Docker API
2376  Docker API TLS
```

---

## 7. 不要暴露 Docker API

不要开放 Docker API 明文端口：

```text
2375
```

这非常危险。

如果远程管理 Docker，一般使用：

* SSH
* VPN
* TLS 保护的 Docker API
* Portainer Agent
* Portainer Edge Agent

普通个人服务器不要随便配置 Docker 监听公网 TCP 端口。

---

## 8. 备份注意事项

Portainer 自身数据一般在：

```text
/data
```

如果你使用目录挂载：

```yaml
- ./portainer_data:/data
```

那么数据就在当前目录下的：

```text
./portainer_data
```

建议定期备份。

备份示例：

```bash
cd /opt/portainer

tar czf portainer_data_backup_$(date +%F).tar.gz ./portainer_data
```

恢复时：

```bash
cd /opt/portainer

docker compose down

mv portainer_data portainer_data_old

tar xzf portainer_data_backup_日期.tar.gz

docker compose up -d
```

注意：Portainer 的备份主要是 Portainer 自身配置和通过 Portainer 管理的 Stack 文件，不等于备份所有业务容器的数据。

例如 MySQL、Redis、应用上传文件等，需要单独备份对应的数据目录或 Volume。

---

## 9. 更新注意事项

更新 Portainer 前，建议先备份：

```bash
cd /opt/portainer

tar czf portainer_data_backup_$(date +%F).tar.gz ./portainer_data
```

然后更新：

```bash
docker compose pull
docker compose up -d
```

查看版本和状态：

```bash
docker ps
docker logs -f portainer
```

如果更新后异常，可以根据备份恢复。

---

## 10. 镜像版本注意事项

不建议所有生产服务都使用：

```text
latest
```

原因：

* 不知道什么时候会升级
* 可能出现兼容性变化
* 回滚困难
* 排查问题不方便

建议使用明确版本：

```yaml
image: mysql:8.0
image: redis:7
image: nginx:1.27
```

对于 Portainer 本身，如果想稳定，可以使用：

```yaml
image: portainer/portainer-ce:lts
```

---

## 11. Stack 使用注意事项

在 Portainer 中使用 Stack 时，需要注意：

1. 部署前先检查 Compose 文件。
2. 不要粘贴来历不明的 Compose。
3. 环境变量中的密码不要太简单。
4. 数据库必须挂载数据目录。
5. 修改 Stack 前先备份原 Compose。
6. 删除 Stack 前确认是否会删除容器和网络。
7. 删除 Volume 前一定要确认里面没有重要数据。

危险操作包括：

```text
删除 Stack
删除 Volume
删除数据库容器
修改端口映射
修改挂载目录
修改网络配置
```

这些操作可能导致服务不可用或数据丢失。

---

## 12. 数据卷注意事项

容器可以删，数据不能乱删。

重点记住：

```text
容器是临时的
镜像可以重新拉
数据卷才是核心资产
```

例如数据库数据通常在：

```yaml
volumes:
  - ./mysql_data:/var/lib/mysql
```

或者：

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

删除这些目录或 Volume，数据库数据就可能丢失。

---

## 13. 端口暴露注意事项

不是所有容器都需要暴露公网端口。

例如：

### 应用需要公网访问

可以暴露：

```yaml
ports:
  - "8080:80"
```

### 数据库只给内部应用访问

不建议暴露：

```yaml
ports:
  - "3306:3306"
```

更推荐只加入同一个 Docker 网络，让应用容器内部访问数据库。

例如：

```yaml
services:
  app:
    image: your-app
    networks:
      - app_network

  mysql:
    image: mysql:8.0
    networks:
      - app_network
    volumes:
      - ./mysql_data:/var/lib/mysql

networks:
  app_network:
    driver: bridge
```

应用连接数据库时使用服务名：

```text
mysql:3306
```

而不是公网 IP。

---

## 14. 容器权限注意事项

尽量避免使用高权限配置：

```yaml
privileged: true
```

除非你知道为什么必须这样做。

也要谨慎使用：

```yaml
network_mode: host
```

以及挂载敏感目录：

```yaml
volumes:
  - /:/host
  - /etc:/etc
  - /root:/root
```

这些配置会显著增加风险。

---

## 15. 日志排查建议

服务异常时，优先查看：

```text
Containers -> 选择容器 -> Logs
```

常见问题包括：

* 端口被占用
* 环境变量错误
* 密码错误
* 数据目录权限不足
* 镜像拉取失败
* 数据库连接失败
* 配置文件路径错误

也可以在服务器上执行：

```bash
docker logs -f 容器名
```

查看 Compose 服务状态：

```bash
docker compose ps
```

---

## 16. 删除操作前检查清单

删除容器前确认：

```text
数据是否已经挂载到外部？
是否有数据库？
是否有上传文件？
是否有配置文件？
是否能重新部署？
```

删除 Stack 前确认：

```text
Compose 文件是否已备份？
数据卷是否会被删除？
端口是否被其他服务接管？
是否影响公网服务？
```

删除 Volume 前确认：

```text
这个 Volume 属于哪个服务？
里面是否有数据库数据？
有没有备份？
是否确定不再需要？
```

---

## 17. 推荐的目录结构

建议把每个项目放到独立目录：

```text
/opt/docker/
  portainer/
    compose.yml
    portainer_data/

  nginx-proxy-manager/
    compose.yml
    data/
    letsencrypt/

  mysql/
    compose.yml
    mysql_data/

  app1/
    compose.yml
    data/
```

好处：

* 结构清晰
* 方便备份
* 方便迁移
* 方便排查问题
* 不同项目互不干扰

---

## 18. 最低安全配置清单

公网使用 Portainer，至少做到：

```text
只开放 9443，不开放 9000
管理员账号使用强密码
不使用 admin/root/test 等常见用户名
云服务器安全组只开放必要端口
系统防火墙只开放必要端口
不开放 Docker API 2375
定期备份 Portainer 数据目录
重要业务数据单独备份
定期更新 Portainer
定期更新系统安全补丁
不运行来历不明的 Compose 文件
不随便删除 Volume
不随便使用 privileged: true
```

---

## 19. 推荐最终部署方式

如果只是个人服务器，推荐：

```text
Portainer 使用 9443
重要服务使用 Stack 管理
数据使用目录挂载或命名卷
公网服务走反向代理
数据库不直接暴露公网
Portainer 尽量限制来源 IP 或走 VPN
```

最终 Portainer Compose 示例：

```yaml
services:
  portainer:
    image: portainer/portainer-ce:lts
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9443:9443"
    networks:
      - portainer_network
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./portainer_data:/data

networks:
  portainer_network:
    name: portainer_network
    driver: bridge
```

启动：

```bash
docker compose up -d
```

访问：

```text
https://你的公网IP:9443
```

---

# 总结

Portainer 可以极大简化 Docker 管理，但它本身是高权限管理入口。

公网使用时必须记住：

```text
方便性越高，暴露风险也越高。
```

建议优先顺序：

```text
VPN 访问 > IP 白名单 > 反向代理 + HTTPS + 认证 > 直接开放 9443
```

不要直接开放 `9000`，不要开放 Docker API，不要使用弱密码，不要删除不清楚用途的 Volume。

真正重要的不是容器，而是数据。容器可以重建，数据丢了很难恢复。
