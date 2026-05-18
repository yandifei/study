根据官方文档，uv 中与文件路径相关的配置主要通过**环境变量**、**默认存储目录**和**项目内文件**三种方式来定义和管理。以下是全面的梳理。

---

### 📁 环境变量配置：所有路径类变量

下表列出了 uv 官方文档中所有与文件路径相关的环境变量。所有环境变量都可通过在命令行前加 `--xxx` 的方式作为参数使用。

| 环境变量 | 作用 |
| :--- | :--- |
| `UV_ASTRAL_MIRROR_URL` | 替换 Astral 相关元数据和产物的下载源 URL。 |
| `UV_BUILD_CONSTRAINT` | 用于构建源码发行版时的约束文件，支持空格分隔的多个文件。 |
| `UV_CACHE_DIR` | 自定义缓存目录，覆盖默认的缓存路径。 |
| `UV_COMPILE_BYTECODE_TIMEOUT` | 设置字节码编译的超时时间（秒）。 |
| `UV_CONFIG_FILE` | 指定 `uv.toml` 配置文件的路径。 |
| `UV_CONSTRAINT` | 通用的约束文件，作用与 `UV_BUILD_CONSTRAINT` 类似。 |
| `UV_CREDENTIALS_DIR` | 当使用明文后端时，用于存储凭证的目录。 |
| `UV_ENV_FILE` | 指定加载环境变量的 `.env` 文件路径。 |
| `UV_EXCLUDE_NEWER` | 排除比指定时间更新的包，可用于要求确定性构建。 |
| `UV_INSTALL_DIR` | 自定义 uv 二进制文件的安装位置。 |
| `UV_INSTALLER_NO_MODIFY_PATH` | 控制安装时是否修改 `PATH` 环境变量。 |
| `UV_LINK_MODE` | 设置安装包的链接方式（clone/copy/hardlink/symlink），影响包的存储效率。 |
| `UV_PYTHON_INSTALL_MIRROR` | 替换 CPython 下载的镜像源。 |
| `UV_PYTHON_PREFERENCE` | 控制 uv 选择 Python 解释器的策略（如仅托管、仅系统等）。 |
| `UV_TOOL_BIN_DIR` | 指定 `uv tool install` 安装的工具的可执行文件目录，需在 `PATH` 中。 |
| `UV_TOOL_DIR` | 指定 `uv tool install` 安装的包和数据目录。 |
| `UV_UNMANAGED_INSTALL` | 将 uv 安装到自定义路径，同时防止安装程序修改 shell 配置。 |

### 💾 默认存储目录：系统级路径规则

uv 遵循 Linux/macOS 的 XDG 规范与 Windows 的已知文件夹规范，其所有数据按用途分类存储于以下目录：

| 目录类型 | 用途 | Linux / macOS 默认路径 |
| :--- | :--- | :--- |
| **缓存目录** | 存储可丢弃但希望长期保留的数据（如依赖包缓存） | `$XDG_CACHE_HOME/uv` 或 `$HOME/.cache/uv` |
| **持久数据目录** | 存储不可丢弃的持久化数据（如 Python 解释器） | `$XDG_DATA_HOME/uv` 或 `$HOME/.local/share/uv` |
| **用户配置目录** | 存储用户级别的配置 | `$XDG_CONFIG_HOME/uv` 或 `$HOME/.config/uv` |
| **系统配置目录** | 存储系统级别的配置 | `$XDG_CONFIG_DIRS/uv` 或 `/etc/uv` |
| **可执行文件目录** | 存储需要加入 `PATH` 的可执行文件 | `$XDG_BIN_HOME`、`$HOME/.local/bin` 等 |
| **临时目录** | 存储临时数据（uv 内部可能使用） | `$TMPDIR` 或 `/tmp` |

> **Windows 用户的默认路径**：缓存目录为 `%LOCALAPPDATA%\uv\cache`，持久数据目录为 `%APPDATA%\uv\data`，系统配置目录为 `%PROGRAMDATA%\uv`。

### 🏗️ 项目级文件：项目内的关键文件

与项目强相关的特殊文件和目录位于项目根目录下：

| 文件/目录 | 作用 |
| :--- | :--- |
| `pyproject.toml` | 核心配置文件，包含项目元数据、依赖、构建系统等信息。 |
| `uv.lock` | 跨平台的锁文件，记录了精确的依赖版本，确保环境一致性。 |
| `.venv/` | 默认的项目虚拟环境目录，位于项目根目录下。 |
| `.env` | 可以放在项目根目录，用于在执行 `uv run` 时加载环境变量。 |

### 🔧 环境路径查找机制

uv 查找环境时遵循特定优先级：

*   **查找位置**：uv 依次查找 `./.venv`、`./.env`（虚拟环境目录）以及通过 `VIRTUAL_ENV` 环境变量指定的路径。若都未找到，则回退到系统 Python 环境。
*   **环境变量指定**：设置 `VIRTUAL_ENV=/path/to/venv` 可强制 uv 使用指定目录作为当前环境。
*   **Python 解释器指定**：使用 `--python /path/to/python` 可让 uv 直接安装到指定解释器对应的环境中。

---

如果您想深入了解 uv 工作流中涉及的某个特定路径或文件，可以告诉我您感兴趣的具体场景，我可以为您进一步解析。