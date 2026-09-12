Dify的源码官网：https://github.com/langgenius/dify

官方中文文档：https://docs.dify.ai/zh/use-dify/getting-started/introduction

---

### 🗄️ 数据保存在哪？

部署完成后，所有的数据和配置会分类存储在如下位置：

| 数据类别           | 存储内容                 | 宿主机存储路径（相对路径）       |
| :----------------- | :----------------------- | :------------------------------- |
| **🧠 核心业务数据** | 用户、应用配置、对话记录 | `./volumes/db/data` (PostgreSQL) |
| **⚡ 缓存与队列**   | 临时数据、任务队列       | `./volumes/redis/data`           |
| **📁 文件存储**     | 上传的图片、文档等       | `./volumes/app/storage`          |
| **📚 向量数据**     | 知识库的向量索引         | `./volumes/weaviate` (默认)      |
| **🔧 插件数据**     | 第三方插件文件           | `./volumes/plugin_daemon`        |
| **🛡️ 其他服务**     | 沙箱、Nginx 日志等       | `./volumes/sandbox`、`./nginx`   |

所有持久化数据都在 `dify/docker/volumes/` 目录下，做好它的备份即可保证数据安全。

---

### 🧭 Dify 全流程部署指南

#### 📝 1. 准备工作

- **硬件要求**：最低 **2核CPU + 4GB 内存**；生产环境推荐 **4核CPU + 8GB 内存以上**。
- **软件要求**：`Docker Engine 19.03+`，`Docker Compose 2.24.0+`。

#### 📦 2. 获取代码与配置

使用终端按顺序执行以下命令。这些步骤直接参考官方文档。

1.  **克隆仓库**
    ```bash
    git clone https://github.com/langgenius/dify.git
    ```

2.  **进入Docker目录**
    ```bash
    cd dify/docker
    ```

3.  **复制配置文件**
    ```bash
    cp .env.example .env
    ```
    这个 `.env` 文件包含了所有核心配置，可按需调整，比如将 `SECRET_KEY` 改成一个复杂的新字符串。

#### 🚀 3. 启动与验证

1.  **启动所有服务**
    ```bash
    docker compose up -d
    ```
    命令会拉取镜像并启动 Dify 的 5 个核心服务（api、worker、web 等）和 6 个依赖组件（数据库、Redis 等）。

2.  **检查运行状态**
    ```bash
    docker compose ps
    ```
    当看到所有服务状态都是 **`Up`** 或 **`healthy`** 时，说明部署成功。

3.  **初始化**
    - 打开浏览器访问 `http://localhost`
    - 如果访问的是远程服务器，将 `localhost` 替换为服务器公网IP。
    - 跟随页面指引，设置管理员邮箱和密码。

---

### 🛠️ 4. 常见问题与技巧

| 场景                    | 原因                 | 解决方法                                                                                     |
| :---------------------- | :------------------- | :------------------------------------------------------------------------------------------- |
| **端口冲突**            | 系统80端口已被占用。 | 修改 `docker-compose.yaml` 中的 `ports: - "8080:80"`，然后用 `8080` 端口访问。               |
| **容器重启后异常**      | 服务启动顺序问题。   | 使用 `docker compose down` 停止，再用 `docker compose up -d` 重启。                          |
| **启动失败 (错误日志)** | 多是权限或配置问题。 | 检查容器日志：`docker compose logs <service_name>`（如 `docker compose logs db_postgres`）。 |
| **使用其他向量数据库**  | 默认使用`weaviate`。 | 在 `.env` 文件中设置 `VECTOR_STORE=your_choice`（如 `milvus`, `pgvector`）。                 |

---

### 🧰 5. 常用管理命令

| 操作                 | 命令                                                   |
| :------------------- | :----------------------------------------------------- |
| **后台启动所有服务** | `docker compose up -d`                                 |
| **停止所有服务**     | `docker compose down`                                  |
| **查看服务状态**     | `docker compose ps`                                    |
| **查看实时日志**     | `docker compose logs -f`                               |
| **进入特定服务容器** | `docker compose exec <服务名> /bin/bash`               |
| **重启所有服务**     | `docker compose restart`                               |
| **停止并删除数据卷** | `docker compose down -v`（危险操作，会清空所有数据！） |

---

### ✅ 6. 部署完成后

1.  **设置环境变量**（可选）：如需对接 OpenAI 以外的模型提供商或设置 S3 存储等，需在 `.env` 文件中配置相应变量。高级配置可参考 `dify/docker/envs/` 目录下的 `.example` 文件。
2.  **配置 HTTPS**：可选操作。设置 `.env` 中的 `NGINX_HTTPS_ENABLED=true`，并将证书放在 `./nginx/ssl` 目录下。
3.  **定期备份**：备份 `dify/docker/volumes/` 和 `dify/docker/.env` 文件，以防数据丢失。
4.  **版本升级**：首先备份数据，然后在 `dify/docker` 目录下依次执行 `docker compose down`，`git pull`，最后执行 `docker compose up -d` 完成升级。