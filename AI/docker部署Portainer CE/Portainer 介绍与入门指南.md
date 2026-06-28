# Portainer 介绍与入门指南

## 1. Portainer 是什么

Portainer 是一个用于管理容器环境的 Web 可视化工具。它可以让你通过浏览器管理 Docker，而不必每次都在服务器上手动输入 `docker`、`docker compose` 等命令。

对于个人服务器、家庭服务器、小型项目部署来说，Portainer 非常适合用来做以下事情：

* 查看和管理容器
* 查看和管理镜像
* 查看容器日志
* 进入容器终端
* 启动、停止、重启、删除容器
* 管理数据卷
* 管理 Docker 网络
* 使用 Compose 文件部署应用
* 通过 Stack 管理一组服务

简单来说，Portainer 可以理解成：**Docker 的 Web 管理面板**。

---

## 2. 适合哪些使用场景

Portainer 比较适合以下场景：

### 2.1 个人服务器

例如你有一台云服务器，想部署：

* Nginx
* MySQL
* Redis
* PostgreSQL
* Alist
* Uptime Kuma
* Nginx Proxy Manager
* Home Assistant
* Jellyfin
* Vaultwarden
* 自己写的后端服务

用 Portainer 可以直接在浏览器里查看和管理这些容器。

### 2.2 不想频繁 SSH 到服务器

如果你平时只是想看看容器是否运行正常、查看日志、重启服务，用 Portainer 会比每次 SSH 登录服务器方便很多。

### 2.3 使用 Docker Compose 管理项目

Portainer 里的 **Stacks** 功能可以直接粘贴或上传 `docker-compose.yml`，然后通过 Web UI 部署整个项目。

---

## 3. Portainer 的核心概念

## 3.1 Environment

Environment 表示一个被 Portainer 管理的容器环境。

常见类型包括：

* Docker Standalone
* Docker Swarm
* Kubernetes

如果你只是普通 Linux 服务器上安装 Docker，一般就是 **Docker Standalone**。

---

## 3.2 Container

Container 就是正在运行或已经停止的容器。

在 Portainer 中，你可以对容器执行：

* Start：启动
* Stop：停止
* Restart：重启
* Kill：强制终止
* Remove：删除
* Logs：查看日志
* Console：进入容器终端
* Inspect：查看容器详细配置

---

## 3.3 Image

Image 是镜像，容器就是由镜像创建出来的。

在 Portainer 中，你可以：

* 查看本地镜像
* 拉取镜像
* 删除镜像
* 查看镜像大小
* 查看镜像标签
* 查看镜像 ID

例如：

* `nginx:latest`
* `mysql:8.0`
* `redis:7`
* `portainer/portainer-ce:lts`

---

## 3.4 Volume

Volume 是 Docker 的数据存储位置。

很多容器的数据必须挂载到 Volume 或宿主机目录，否则容器删除后数据也可能丢失。

常见例子：

```yaml
volumes:
  - ./mysql_data:/var/lib/mysql
```

或者：

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

Portainer 可以查看、创建和删除 Docker Volume。

---

## 3.5 Network

Network 是 Docker 容器之间通信的网络。

常见网络类型是：

* bridge
* host
* none
* overlay

个人服务器上最常见的是 `bridge` 网络。

如果多个容器需要互相访问，例如应用容器访问数据库容器，通常应该让它们加入同一个 Docker 网络。

---

## 3.6 Stack

Stack 是 Portainer 中非常重要的概念。

可以简单理解为：**一个 docker-compose.yml 管理的一组服务**。

例如一个 WordPress 项目可能包含：

* WordPress 容器
* MySQL 容器
* Nginx 容器
* 数据卷
* 网络配置

这些服务合在一起，就可以作为一个 Stack 管理。

---

## 4. 使用 Docker Compose 部署 Portainer

推荐使用 Docker Compose 部署 Portainer，方便后期维护、升级和迁移。

新建目录：

```bash
mkdir -p /opt/portainer
cd /opt/portainer
```

创建 `compose.yml`：

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

查看容器状态：

```bash
docker ps
```

查看日志：

```bash
docker logs -f portainer
```

访问：

```text
https://你的服务器公网IP:9443
```

首次打开时，浏览器可能提示证书不安全，这是因为默认使用自签名 HTTPS 证书。确认是自己的服务器后，可以继续访问。

---

## 5. 第一次进入 Portainer

首次访问 Portainer 时，一般需要完成以下步骤：

1. 创建管理员账号
2. 设置强密码
3. 选择要管理的 Docker 环境
4. 进入本地 Docker 环境
5. 开始管理容器、镜像、网络和数据卷

建议管理员账号不要使用简单用户名，例如不要使用：

```text
admin
root
test
```

建议使用不容易猜到的用户名和强密码。

---

## 6. 常用功能入口

## 6.1 查看容器

进入：

```text
Environment -> Containers
```

这里可以看到所有容器，包括运行中的和已经停止的容器。

常用操作：

* 查看状态
* 重启容器
* 停止容器
* 查看日志
* 进入终端
* 删除容器

---

## 6.2 查看日志

进入：

```text
Containers -> 选择容器 -> Logs
```

适合排查服务启动失败、端口冲突、配置错误等问题。

---

## 6.3 进入容器终端

进入：

```text
Containers -> 选择容器 -> Console
```

常见命令：

```bash
sh
```

或者：

```bash
bash
```

不是所有容器都有 `bash`，很多轻量镜像只有 `sh`。

---

## 6.4 管理镜像

进入：

```text
Environment -> Images
```

可以做：

* 拉取镜像
* 删除镜像
* 查看镜像大小
* 查看镜像标签

例如拉取镜像：

```text
nginx:latest
redis:7
mysql:8.0
```

---

## 6.5 管理数据卷

进入：

```text
Environment -> Volumes
```

这里可以查看所有 Docker Volume。

注意：删除 Volume 可能导致应用数据丢失，例如数据库数据、应用配置、上传文件等。

---

## 6.6 管理网络

进入：

```text
Environment -> Networks
```

可以创建网络、删除网络、查看容器连接情况。

常见建议：

* 一个项目用一个独立网络
* 不相关的服务不要随便放到同一个网络
* 数据库端口不一定要暴露到公网，只需要让应用容器能访问即可

---

## 7. 使用 Stack 部署应用

进入：

```text
Stacks -> Add stack
```

填写 Stack 名称，例如：

```text
nginx-demo
```

然后粘贴 Compose 内容：

```yaml
services:
  nginx:
    image: nginx:latest
    container_name: nginx-demo
    restart: unless-stopped
    ports:
      - "8080:80"
```

点击部署后，Portainer 会自动创建容器。

访问：

```text
http://你的服务器IP:8080
```

---

## 8. Stack 的基本维护

进入：

```text
Stacks -> 选择某个 Stack
```

可以进行：

* 查看 Stack 服务
* 修改 Compose 文件
* 重新部署
* 停止 Stack
* 删除 Stack

建议所有正式服务尽量用 Stack 管理，而不是手动创建零散容器。

原因是 Stack 有完整的 Compose 配置，后期迁移和恢复更方便。

---

## 9. 常见项目部署模板

## 9.1 Nginx 示例

```yaml
services:
  nginx:
    image: nginx:latest
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
```

---

## 9.2 Redis 示例

```yaml
services:
  redis:
    image: redis:7
    container_name: redis
    restart: unless-stopped
    volumes:
      - ./redis_data:/data
    command: redis-server --appendonly yes
```

---

## 9.3 MySQL 示例

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: 请改成强密码
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: 请改成强密码
    volumes:
      - ./mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
```

注意：数据库端口不建议直接暴露公网。如果只是给同一台服务器上的应用使用，可以不写 `ports`。

---

## 10. 日常使用建议

1. 新项目优先使用 Stack 部署。
2. 重要数据必须挂载 Volume 或宿主机目录。
3. 删除容器前确认数据是否在外部持久化。
4. 不要随便删除 Volume。
5. 不要直接使用来历不明的镜像。
6. 镜像尽量指定明确版本，不要所有服务都用 `latest`。
7. 修改 Compose 文件前，先备份原配置。
8. 公网暴露服务前，先确认认证、端口和防火墙。
9. 定期更新 Portainer 和关键业务镜像。
10. 重要服务要单独做数据备份。

---

## 11. 常用命令备忘

进入 Portainer 部署目录：

```bash
cd /opt/portainer
```

启动：

```bash
docker compose up -d
```

停止：

```bash
docker compose down
```

查看日志：

```bash
docker logs -f portainer
```

更新：

```bash
docker compose pull
docker compose up -d
```

查看 Docker 占用空间：

```bash
docker system df
```

清理无用资源：

```bash
docker system prune
```

谨慎清理所有未使用镜像：

```bash
docker image prune -a
```

---

# 总结

Portainer 适合用来可视化管理 Docker，尤其适合个人服务器和中小型项目。

推荐使用方式：

```text
Docker Compose 部署 Portainer
Portainer 管理 Stacks
Stacks 管理业务服务
重要数据使用 Volume 或目录持久化
公网访问时加强安全措施
```

Portainer 可以提升 Docker 管理效率，但它不是安全防护工具。真正上线使用时，仍然需要做好密码、防火墙、HTTPS、备份和权限管理。
