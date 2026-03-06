资料参考：
https://docs.openwebui.com/
https://github.com/open-webui/open-webui

我在电脑本地部署过openweb-ui了，但不是docker部署的，接下来记录2种部署方式，并实践第二种部署方式。

# 电脑python虚拟环境部署
创建虚拟环境
```bash
conda create -n openweb-ui python=3.13.5
```
激活虚拟环境
```bash
conda activate openweb-ui
```
安装openweb-ui
```bash
pip install open-webui
```
启动
```bash
open-webui serve
```
访问 http://localhost:8080

# docker部署
### 🐳 基础与通用部署
适用于大多数标准场景的Docker运行命令。

| 场景                        | Docker命令                                                                                                                                                                                 | 说明                           |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- |
| **标准安装** (Ollama在本机) | `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`            | 连接宿主机上的Ollama。         |
| **支持NVIDIA GPU**          | `docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda` | 启用GPU加速。                  |
| **精简镜像** (无预装模型)   | `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main-slim`       | 镜像更小，模型首次使用时下载。 |

### 📦 与Ollama捆绑安装
此方法在一个容器中同时运行Open WebUI和Ollama。

| 场景          | Docker命令                                                                                                                                                              | 说明                          |
| :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------- |
| **带GPU支持** | `docker run -d -p 3000:8080 --gpus=all -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama` | 一体化安装，适合有GPU的环境。 |
| **仅CPU**     | `docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama`            | 一体化安装，适合无GPU的环境。 |

### 🧪 开发分支 (Dev Branch)
运行最新的开发版本以进行测试。

| 场景               | Docker命令                                                                                                                             | 说明                       |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------- | :------------------------- |
| **标准开发镜像**   | `docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:dev`      | 包含最新功能，可能不稳定。 |
| **开发版精简镜像** | `docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:dev-slim` | 开发版的精简变体。         |

# 🔄 更新Open WebUI
使用Watchtower工具管理容器更新。

| 更新方式               | Docker命令                                                                                                                                             | 说明               |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| **手动更新**           | `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nickfedor/watchtower --run-once open-webui`                                              | 执行一次更新。     |
| **自动更新** (每5分钟) | `docker run -d --name watchtower --restart unless-stopped -v /var/run/docker.sock:/var/run/docker.sock nickfedor/watchtower --interval 300 open-webui` | 定期自动检查更新。 |

### 💡 重要说明与提示
1.  **镜像仓库**：文档中使用的`ghcr.io/open-webui/open-webui`可以替换为`openwebui/open-webui` (Docker Hub)，两者镜像内容相同。
2.  **WebSocket支持**：Open WebUI正常运行需要WebSocket支持，请确保你的网络配置允许。
3.  **生产环境标签**：对于生产环境，建议固定使用**特定版本号**（如`v0.8.6`）的镜像，而不是`main`或`cuda`这类浮动标签，以保证稳定性。格式如：`ghcr.io/open-webui/open-webui:v0.8.6-cuda`。
4.  **开发测试数据**：运行`dev`分支镜像时，**切勿**与生产环境共享数据卷，应使用独立的数据卷（如`-v open-webui-dev:/app/backend/data`）进行测试，避免数据库迁移不兼容导致的问题。
5.  **访问地址**：容器启动成功后，通常可以通过 `http://localhost:3000` 访问Open WebUI。
6.  

***

### 💾 数据持久化参数

容器默认是临时的，删除后所有数据都会丢失。通过数据卷（volume）可以将容器内的数据保存到宿主机上，实现持久化。

| 参数                              | 含义                                     | 作用                                                                                                                                                                                                                            |
| :-------------------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-v open-webui:/app/backend/data` | **挂载数据卷**                           | 创建一个名为 `open-webui` 的 Docker 卷，并将其挂载到容器内的 `/app/backend/data` 目录。这个目录存放了 Open WebUI 的所有数据（用户信息、聊天记录、配置等）。即使容器被删除，数据卷里的数据依然保留，下次启动时可以重新挂载恢复。 |
| `-v ollama:/root/.ollama`         | **挂载 Ollama 数据卷**（捆绑安装时使用） | 同样创建一个名为 `ollama` 的卷，挂载到容器内的 `/root/.ollama` 目录。这个目录是 Ollama 存储模型和配置的地方。使用捆绑镜像时，必须挂载此卷，否则每次重启容器都会丢失已下载的模型。                                               |

> **卷 vs 绑定挂载**：这里使用的是 Docker 管理的卷（volume），由 Docker 自动在宿主机某个目录下创建和管理，比直接绑定宿主机路径（如 `-v /home/user/data:/app/backend/data`）更安全、更易于备份。

### 📦 镜像标签（Tags）的含义

命令最后一部分是镜像名称和标签，例如 `ghcr.io/open-webui/open-webui:main`。不同标签代表了不同的构建版本和功能组合。

| 标签             | 含义                     | 适用场景                                                                                                    |
| :--------------- | :----------------------- | :---------------------------------------------------------------------------------------------------------- |
| `:main`          | **主分支最新稳定版**     | 标准的稳定版本，不包含 GPU 专用驱动或 Ollama 捆绑。适合连接外部 Ollama 服务（宿主机或远程）。               |
| `:cuda`          | **包含 CUDA 支持的版本** | 镜像内预装了 CUDA 运行时，便于使用 GPU 加速。适合需要 GPU 加速且连接外部 Ollama 的场景。                    |
| `:ollama`        | **捆绑 Ollama 的版本**   | 镜像内同时包含了 Open WebUI 和 Ollama，一个容器跑两个服务。适合希望一键部署、不需要单独运行 Ollama 的用户。 |
| `:main-slim`     | **精简版主分支**         | 移除了预装的一些模型文件，镜像体积更小，但首次使用模型时需要下载。适合网络较好、希望节省存储空间的场景。    |
| `:dev`           | **开发分支最新版**       | 包含最新的未稳定功能，可能存在问题，仅用于测试和贡献。                                                      |
| `:dev-slim`      | **开发分支精简版**       | 开发分支的精简版本。                                                                                        |
| `:v0.8.6` (示例) | **固定版本号**           | 生产环境推荐使用固定版本号（如 `v0.8.6`），而不是浮动标签（如 `main`），以确保环境一致性和稳定性。          |

### 🔍 总结与选择建议

- **如果你已在宿主机运行 Ollama** → 使用 `:main` 或 `:cuda`（带 GPU 则用 `:cuda`），并加上 `--add-host` 参数让容器能找到宿主机 Ollama。
- **希望一切都在容器内** → 使用 `:ollama` 标签，并挂载两个卷（`open-webui` 和 `ollama`），根据需要决定是否加 `--gpus`。
- **生产环境** → 使用固定版本标签（如 `:v0.8.6`），配合 `--restart always`，确保稳定性。
- **仅测试最新功能** → 使用 `:dev` 或 `:dev-slim`，但务必使用独立的数据卷，避免影响生产数据。

