# from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any,Sequence
# 第三方库
from playwright.sync_api import ProxySettings
from pydantic import BaseModel
# 自己的模块
# from utils import debug

class LaunchOptions(BaseModel):
    """浏览器启动选项配置类
    # 注意：Playwright 只保证与捆绑的 Chromium、Firefox 或 WebKit 正常工作，使用此选项需自行承担风险。
    executable_path: Path | str | None = None
    # 浏览器发行渠道。
    # 设置为 "chromium" 以启用新的无头模式
    # 可设置为 "chrome"、"chrome-beta"、"chrome-dev"、"chrome-canary"、"msedge"、
    # "msedge-beta"、"msedge-dev" 或 "msedge-canary" 来使用官方的 Google Chrome 或 Microsoft Edge
    channel: str | None = None
    # 传递给浏览器实例的额外命令行参数。
    # 警告：使用自定义浏览器参数需自行承担风险，某些参数可能会破坏 Playwright 功能。
    # Chromium 的可用参数列表：https://peter.sh/experiments/chromium-command-line-switches/
    args: Sequence[str] | None = None
    # 如果为 True，Playwright 将不传递其默认配置参数，只使用 args 中的参数。
    # 如果为数组，则过滤掉指定的默认参数。此为危险选项，请谨慎使用。默认值为 False。
    ignore_default_args: bool | Sequence[str] | None = False
    # 在收到 Ctrl-C 时关闭浏览器进程。默认值为 True。
    handle_sigint: bool | None = True
    # 在收到 SIGTERM 信号时关闭浏览器进程。默认值为 True。
    handle_sigterm: bool | None = True
    # 在收到 SIGHUP 信号时关闭浏览器进程。默认值为 True。
    handle_sighup: bool | None = True
    # 等待浏览器实例启动的最大时间（毫秒）。默认值为 30000（30秒）。设置为 0 表示禁用超时。
    timeout: float | None = 30000
    # 指定浏览器可见的环境变量。默认使用 process.env。
    env: dict[str, str | float | bool] | None = None  # 默认 None，内部使用 process.env
    # 是否以无头模式运行浏览器。
    # 如果 devtools 选项为 True，则此选项默认为 False，否则默认为 True。
    headless: bool | None = None  # 默认 None，内部根据 devtools 自动处理
    # 仅限 Chromium：是否为每个标签页自动打开开发者工具面板。
    # 如果此选项为 True，headless 选项将被设置为 False。
    # 已弃用：建议使用调试工具代替。
    devtools: bool | None = False
    # 网络代理设置。
    proxy: ProxySettings | None = None
    # 如果指定，已接受的下载将保存到此目录。
    # 否则将创建临时目录，并在浏览器关闭时删除。
    # 无论哪种情况，下载都会在创建它们的浏览器上下文关闭时被删除。
    downloads_path: Path | str | None = None
    # 以指定的毫秒数减慢 Playwright 操作速度。
    # 有助于观察正在进行的操作。
    slow_mo: float | None = 0
    # 如果指定，跟踪记录将保存到此目录。
    traces_dir: Path | str | None = None
    # 启用 Chromium 沙盒。默认值为 False。
    chromium_sandbox: bool | None = False
    # Firefox 用户偏好设置。可在 about:config 页面了解 Firefox 用户偏好设置。
    # 也可以通过 PLAYWRIGHT_FIREFOX_POLICIES_JSON 环境变量提供自定义的 policies.json 文件路径。
    firefox_user_prefs: dict[str, str | float | bool] | None = None
    """
    # 注意：Playwright 只保证与捆绑的 Chromium、Firefox 或 WebKit 正常工作，使用此选项需自行承担风险。
    executable_path: Path | str | None = None
    # 浏览器发行渠道。
    # 设置为 "chromium" 以启用新的无头模式
    # 可设置为 "chrome"、"chrome-beta"、"chrome-dev"、"chrome-canary"、"msedge"、
    # "msedge-beta"、"msedge-dev" 或 "msedge-canary" 来使用官方的 Google Chrome 或 Microsoft Edge
    channel: str | None = None
    # 传递给浏览器实例的额外命令行参数。
    # 警告：使用自定义浏览器参数需自行承担风险，某些参数可能会破坏 Playwright 功能。
    # Chromium 的可用参数列表：https://peter.sh/experiments/chromium-command-line-switches/
    args: Sequence[str] | None = None
    # 如果为 True，Playwright 将不传递其默认配置参数，只使用 args 中的参数。
    # 如果为数组，则过滤掉指定的默认参数。此为危险选项，请谨慎使用。默认值为 None。
    ignore_default_args: bool | Sequence[str] | None = None
    # 在收到 Ctrl-C 时关闭浏览器进程。默认值为 True。
    handle_sigint: bool | None = True
    # 在收到 SIGTERM 信号时关闭浏览器进程。默认值为 True。
    handle_sigterm: bool | None = True
    # 在收到 SIGHUP 信号时关闭浏览器进程。默认值为 True。
    handle_sighup: bool | None = True
    # 等待浏览器实例启动的最大时间（毫秒）。默认值为 30000（30秒）。设置为 0 表示禁用超时。
    timeout: float | None = 30000
    # 指定浏览器可见的环境变量。默认使用 process.env。
    env: dict[str, str | float | bool] | None = None  # 默认 None，内部使用 process.env
    # 是否以无头模式运行浏览器。
    # 如果 devtools 选项为 True，则此选项默认为 False，否则默认为 True。
    headless: bool | None = None  # 默认 None，内部根据 devtools 自动处理
    # 仅限 Chromium：是否为每个标签页自动打开开发者工具面板。
    # 如果此选项为 True，headless 选项将被设置为 False。
    # 已弃用：建议使用调试工具代替。
    devtools: bool | None = False
    # 网络代理设置。
    proxy: ProxySettings | None = None
    # 如果指定，已接受的下载将保存到此目录。
    # 否则将创建临时目录，并在浏览器关闭时删除。
    # 无论哪种情况，下载都会在创建它们的浏览器上下文关闭时被删除。
    downloads_path: Path | str | None = None
    # 以指定的毫秒数减慢 Playwright 操作速度。
    # 有助于观察正在进行的操作。
    slow_mo: float | None = 0
    # 如果指定，跟踪记录将保存到此目录。
    traces_dir: Path | str | None = None
    # 启用 Chromium 沙盒。默认值为 False。
    chromium_sandbox: bool | None = False
    # Firefox 用户偏好设置。可在 about:config 页面了解 Firefox 用户偏好设置。
    # 也可以通过 PLAYWRIGHT_FIREFOX_POLICIES_JSON 环境变量提供自定义的 policies.json 文件路径。
    firefox_user_prefs: dict[str, str | float | bool] | None = None

    # def to_dict(self) -> dict[str, Any]:
    #     # 转换为字典格式，过滤掉None值
    #     return {k: v for k, v in asdict(self).items() if v is not None}