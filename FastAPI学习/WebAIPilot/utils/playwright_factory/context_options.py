from pathlib import Path
from typing import Sequence, Pattern, Literal
# 第三方库
from playwright.async_api import ViewportSize, Geolocation, HttpCredentials, ProxySettings, StorageState
from playwright._impl._api_structures import ClientCertificate
from pydantic import BaseModel, Field


class ContextOptions(BaseModel):
    """浏览器上下文选项配置类
    用于配置浏览器上下文的各种参数，如视口大小、JavaScript启用状态、代理设置等。
    所有参数都提供了与Playwright官方文档一致的默认值。
    # 设置每个页面的固定视口大小。默认为1280x720视口。no_viewport参数可禁用固定视口。
    viewport: ViewportSize | None = field(
        default_factory=lambda: {"width": 1280, "height": 720}
    )
    # 通过window.screen模拟网页内可用的窗口屏幕大小。仅在设置viewport时使用。
    screen: ViewportSize | None = None
    # 不强制执行固定视口，允许在headed模式下调整窗口大小。
    no_viewport: bool | None = False
    # 发送网络请求时是否忽略HTTPS错误。默认为false。
    ignore_https_errors: bool | None = False
    # 是否在上下文中启用JavaScript。默认为true。
    java_script_enabled: bool | None = True
    # 是否绕过页面的内容安全策略。默认为false。
    bypass_csp: bool | None = False
    # 在此上下文中使用的特定用户代理字符串。
    user_agent: str | None = None
    # 指定用户区域设置，例如en-GB, de-DE等。区域设置会影响navigator.language值、Accept-Language请求头值以及数字和日期格式化规则。默认为系统默认区域设置。
    locale: str | None = None
    # 更改上下文的时区。支持时区ID列表请参考ICU的metaZones.txt。默认为系统时区。
    timezone_id: str | None = None
    # 地理位置信息，包括纬度和经度。
    geolocation: Geolocation | None = None
    # 授予此上下文中所有页面的权限列表。默认为无。
    permissions: Sequence[str] | None = None
    # 包含要随每个请求发送的额外HTTP头的对象。默认为无。
    extra_http_headers: dict[str, str] | None = None
    # 是否模拟网络离线状态。默认为false。
    offline: bool | None = False
    # HTTP身份验证的凭据。如果未指定来源，则在收到未经授权的响应时，用户名和密码将发送到任何服务器。
    http_credentials: HttpCredentials | None = None
    # 指定设备缩放因子（可视为dpr）。默认为1。
    device_scale_factor: float | None = 1.0
    # 是否考虑meta viewport标签并启用触摸事件。isMobile是设备的一部分，因此实际上不需要手动设置它。默认为false，Firefox不支持。
    is_mobile: bool | None = False
    # 指定视口是否支持触摸事件。默认为false。
    has_touch: bool | None = False
    # 模拟prefers-colors-scheme媒体功能，支持的值有'light'、'dark'。传递'null'将重置为系统默认值。默认为'light'。
    color_scheme: Literal["dark", "light", "no-preference", "null"] | None = "light"
    # 模拟'prefers-reduced-motion'媒体功能，支持的值有'reduce'、'no-preference'。传递'null'将重置为系统默认值。默认为'no-preference'。
    reduced_motion: Literal["no-preference", "null", "reduce"] | None = "no-preference"
    # 模拟'forced-colors'媒体功能，支持的值有'active'、'none'。传递'null'将重置为系统默认值。默认为'none'。
    forced_colors: Literal["active", "none", "null"] | None = "none"
    # 模拟'prefers-contrast'媒体功能，支持的值有'no-preference'、'more'。传递'null'将重置为系统默认值。默认为'no-preference'。
    contrast: Literal["more", "no-preference", "null"] | None = "no-preference"
    # 是否自动下载所有附件。默认为true，接受所有下载。
    accept_downloads: bool | None = True
    # 默认浏览器类型。此参数未在文档中明确说明默认值。
    default_browser_type: str | None = None
    # 与此上下文一起使用的网络代理设置。默认为无。
    proxy: ProxySettings | None = None
    # 为所有页面启用HAR记录，将HAR文件保存到文件系统的指定路径。如果未指定，则不记录HAR。确保调用browser_context.close()以保存HAR。
    record_har_path: Path | str | None = None
    # 可选设置，控制是否从HAR中省略请求内容。默认为false。
    record_har_omit_content: bool | None = False
    # 为所有页面启用视频录制，将视频保存到指定目录。如果未指定，则不录制视频。确保调用browser_context.close()以保存视频。
    record_video_dir: Path | str | None = None
    # 录制视频的尺寸。如果未指定，尺寸将等于视口按比例缩小以适合800x800。如果未显式配置视口，视频尺寸默认为800x450。
    record_video_size: ViewportSize | None = None
    # 用给定的存储状态填充上下文。此选项可用于使用通过browser_context.storage_state()获取的已登录信息初始化上下文。
    storage_state: StorageState | str | Path | None = None
    # 在使用page.goto()、page.route()、page.wait_for_url()、page.expect_request()或page.expect_response()时，会通过使用URL()构造函数构建相应的URL来考虑基础URL。默认未设置。
    base_url: str | None = None
    # 如果设置为true，则为此上下文启用严格选择器模式。在严格选择器模式下，所有意味着单个目标DOM元素的选择器操作在多个元素匹配选择器时将抛出异常。此选项不影响任何定位器API（定位器始终是严格的）。默认为false。
    strict_selectors: bool | None = False
    # 是否允许站点注册Service workers。默认为'allow'。'allow'：可以注册Service Workers；'block'：Playwright将阻止所有Service Workers的注册。
    service_workers: Literal["allow", "block"] | None = "allow"
    # 记录HAR时的URL过滤器，可以是正则表达式模式或字符串。
    record_har_url_filter: Pattern[str] | str | None = None
    # 当设置为minimal时，仅记录从HAR进行路由所必需的信息。这会省略大小、时间、页面、cookie、安全和其他在从HAR重放时不使用的HAR信息类型。默认为full。
    record_har_mode: Literal["full", "minimal"] | None = "full"
    # 控制资源内容管理的可选设置。如果指定omit，则不保留内容。如果指定attach，则资源作为单独文件保留，所有这些文件都与HAR文件一起存档。默认为embed，根据HAR规范将内容内联存储在HAR文件中。
    record_har_content: Literal["attach", "embed", "omit"] | None = "embed"
    # TLS客户端身份验证，允许服务器请求客户端证书并进行验证。要使用的客户端证书数组。当提供至少一个客户端证书时，客户端证书身份验证才处于活动状态。
    client_certificates: list[ClientCertificate] | None = None
    """

    # 设置每个页面的固定视口大小。默认为1280x720视口。no_viewport参数可禁用固定视口。
    # viewport: ViewportSize | None = Field(
    #     default={"width": 1280, "height": 720},
    #     description="设置每个页面的固定视口大小"
    # )
    viewport: ViewportSize | None = None
    # 通过window.screen模拟网页内可用的窗口屏幕大小。仅在设置viewport时使用。
    screen: ViewportSize | None = None
    # 不强制执行固定视口，允许在headed模式下调整窗口大小。
    no_viewport: bool | None = False
    # 发送网络请求时是否忽略HTTPS错误。默认为false。
    ignore_https_errors: bool | None = False
    # 是否在上下文中启用JavaScript。默认为true。
    java_script_enabled: bool | None = True
    # 是否绕过页面的内容安全策略。默认为false。
    bypass_csp: bool | None = False
    # 在此上下文中使用的特定用户代理字符串。
    user_agent: str | None = None
    # 指定用户区域设置，例如en-GB, de-DE等。区域设置会影响navigator.language值、Accept-Language请求头值以及数字和日期格式化规则。默认为系统默认区域设置。
    locale: str | None = None
    # 更改上下文的时区。支持时区ID列表请参考ICU的metaZones.txt。默认为系统时区。
    timezone_id: str | None = None
    # 地理位置信息，包括纬度和经度。
    geolocation: Geolocation | None = None
    # 授予此上下文中所有页面的权限列表。默认为无。
    permissions: Sequence[str] | None = None
    # 包含要随每个请求发送的额外HTTP头的对象。默认为无。
    extra_http_headers: dict[str, str] | None = None
    # 是否模拟网络离线状态。默认为false。
    offline: bool | None = False
    # HTTP身份验证的凭据。如果未指定来源，则在收到未经授权的响应时，用户名和密码将发送到任何服务器。
    http_credentials: HttpCredentials | None = None
    # 指定设备缩放因子（可视为dpr）。默认为1。
    device_scale_factor: float | None = 1.0
    # 是否考虑meta viewport标签并启用触摸事件。isMobile是设备的一部分，因此实际上不需要手动设置它。默认为false，Firefox不支持。
    is_mobile: bool | None = False
    # 指定视口是否支持触摸事件。默认为false。
    has_touch: bool | None = False
    # 模拟prefers-colors-scheme媒体功能，支持的值有'light'、'dark'。传递'null'将重置为系统默认值。默认为'light'。
    color_scheme: Literal["dark", "light", "no-preference", "null"] | None = "light"
    # 模拟'prefers-reduced-motion'媒体功能，支持的值有'reduce'、'no-preference'。传递'null'将重置为系统默认值。默认为'no-preference'。
    reduced_motion: Literal["no-preference", "null", "reduce"] | None = "no-preference"
    # 模拟'forced-colors'媒体功能，支持的值有'active'、'none'。传递'null'将重置为系统默认值。默认为'none'。
    forced_colors: Literal["active", "none", "null"] | None = "none"
    # 模拟'prefers-contrast'媒体功能，支持的值有'no-preference'、'more'。传递'null'将重置为系统默认值。默认为'no-preference'。
    contrast: Literal["more", "no-preference", "null"] | None = "no-preference"
    # 是否自动下载所有附件。默认为true，接受所有下载。
    accept_downloads: bool | None = True
    # 默认浏览器类型。此参数未在文档中明确说明默认值。
    default_browser_type: str | None = None
    # 与此上下文一起使用的网络代理设置。默认为无。
    proxy: ProxySettings | None = None
    # 为所有页面启用HAR记录，将HAR文件保存到文件系统的指定路径。如果未指定，则不记录HAR。确保调用browser_context.close()以保存HAR。
    record_har_path: Path | str | None = None
    # 可选设置，控制是否从HAR中省略请求内容。默认为false。
    record_har_omit_content: bool | None = False
    # 为所有页面启用视频录制，将视频保存到指定目录。如果未指定，则不录制视频。确保调用browser_context.close()以保存视频。
    record_video_dir: Path | str | None = None
    # 录制视频的尺寸。如果未指定，尺寸将等于视口按比例缩小以适合800x800。如果未显式配置视口，视频尺寸默认为800x450。
    record_video_size: ViewportSize | None = None
    # 用给定的存储状态填充上下文。此选项可用于使用通过browser_context.storage_state()获取的已登录信息初始化上下文。
    storage_state: StorageState | str | Path | None = None
    # 在使用page.goto()、page.route()、page.wait_for_url()、page.expect_request()或page.expect_response()时，会通过使用URL()构造函数构建相应的URL来考虑基础URL。默认未设置。
    base_url: str | None = None
    # 如果设置为true，则为此上下文启用严格选择器模式。在严格选择器模式下，所有意味着单个目标DOM元素的选择器操作在多个元素匹配选择器时将抛出异常。此选项不影响任何定位器API（定位器始终是严格的）。默认为false。
    strict_selectors: bool | None = False
    # 是否允许站点注册Service workers。默认为'allow'。'allow'：可以注册Service Workers；'block'：Playwright将阻止所有Service Workers的注册。
    service_workers: Literal["allow", "block"] | None = "allow"
    # 记录HAR时的URL过滤器，可以是正则表达式模式或字符串。
    record_har_url_filter: Pattern[str] | str | None = None
    # 当设置为minimal时，仅记录从HAR进行路由所必需的信息。这会省略大小、时间、页面、cookie、安全和其他在从HAR重放时不使用的HAR信息类型。默认为full。
    record_har_mode: Literal["full", "minimal"] | None = "full"
    # 控制资源内容管理的可选设置。如果指定omit，则不保留内容。如果指定attach，则资源作为单独文件保留，所有这些文件都与HAR文件一起存档。默认为embed，根据HAR规范将内容内联存储在HAR文件中。
    record_har_content: Literal["attach", "embed", "omit"] | None = "embed"
    # TLS客户端身份验证，允许服务器请求客户端证书并进行验证。要使用的客户端证书数组。当提供至少一个客户端证书时，客户端证书身份验证才处于活动状态。
    client_certificates: list[ClientCertificate] | None = None

    # def to_dict(self) -> dict[str, Any]:
    #     """转换为字典格式，过滤掉None值"""
    #     return {k: v for k, v in asdict(self).items() if v is not None}