# 内置库
from pathlib import Path
from typing import Literal
# 第三方库
from pydantic import BaseModel
# 自己的模块
from data_models.playwright.context_options import ContextOptions
from data_models.playwright.launch_options import LaunchOptions

class PlaywrightConfig(BaseModel):
    """Playwright 配置"""
    # chromium, firefox, webkit
    browser_type: Literal["chromium", "firefox", "webkit"] = "chromium"
    # 截图路径保存
    screen_dir: str | Path = "outputs/screenshots"
    # js的内存上限,默认4GB（GB）
    node_memory: int = 4096
    # 浏览器上下文选项配置
    context_options: ContextOptions
    # 浏览器启动选项配置
    launch_options: LaunchOptions

