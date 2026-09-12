# 获取系统变量
import os
# smtplib 是 Python 内置的 SMTP 协议客户端库，用于连接邮件服务器并发送邮件
import smtplib
from datetime import time
# MIMEText 用于构造纯文本或 HTML 格式的邮件正文内容（MIME 是邮件扩展标准，定义邮件格式）
from email.mime.text import MIMEText
# MIMEImage 用于构造图片附件
from email.mime.image import MIMEImage
# MIMEMultipart 用于构造包含多个部分（如正文、附件等）的复合邮件对象
from email.mime.multipart import MIMEMultipart
# 随机数生成
import random
# 时间获取
from datetime import datetime
# 获取根目录函数
from utils.path_utils import get_root
# 路径
from pathlib import Path
# 日志
from logger import warning, info
# 类型标注
from typing import List, Optional


# ============================================================
# 内部辅助函数
# ============================================================

def _build_and_send(email: str, subject: str, html: str) -> bool:
    """
    构建 MIME 邮件对象并发送（所有发送方法的公共底层）。

    Args:
        email: 收件人邮箱地址
        subject: 邮件主题
        html: 已渲染的 HTML 正文

    Returns:
        True 表示发送成功，False 表示发送失败
    """
    msg = MIMEMultipart('related')
    msg["From"] = os.getenv("SENDER_EMAIL", "")
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(html, "html"))

    # 附加图片
    with open(Path(get_root(), "config/logo.png"), "rb") as f:
        img = MIMEImage(f.read())
    img.add_header("Content-ID", "<logo>")
    msg.attach(img)

    try:
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(os.getenv("SENDER_EMAIL", ""), os.getenv("SMTP", ""))
            server.sendmail(os.getenv("SENDER_EMAIL", ""), email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        warning("授权码错误或未开启 SMTP 服务")
        return False
    except ConnectionRefusedError:
        warning("网络不通或端口被防火墙拦截")
        return False
    except Exception as e:
        warning({"message": e})
        return False
    else:
        info(f"向{email}用户发送邮件发送成功")
        return True


def _load_template(template_name: str) -> str:
    """加载指定模板文件并返回 HTML 字符串"""
    with open(Path(get_root(), f"templates/{template_name}.html"), "r", encoding="utf-8") as f:
        return f.read()


def _replace_common(html: str) -> str:
    """替换公共占位符：time 和 app_name"""
    html = html.replace("{time}", f"{datetime.now().year}")
    html = html.replace("{app_name}", os.getenv("APP_NAME", ""))
    return html


# ============================================================
# 1. 验证码邮件（已有）
# ============================================================

def send_verification_email(email: str, verification_num: str) -> None:
    """
    发送验证码邮件

    通过 QQ 邮箱 SMTP 服务器向指定邮箱发送包含验证码的 HTML 格式邮件。
    邮件内容使用模板渲染，包含验证码、当前年份和应用名称。

    Args:
        email: 收件人邮箱地址，例如: "user@example.com"
        verification_num: 6位数字验证码，可通过以下代码生成:
                         ''.join(random.choices('0123456789', k=6))

    Returns:
        None

    Raises:
        smtplib.SMTPAuthenticationError: 授权码错误或未开启 SMTP 服务
        ConnectionRefusedError: 网络不通或端口被防火墙拦截
        Exception: 其他邮件发送异常

    Example:
        >>> import random
        >>> code = ''.join(random.choices('0123456789', k=6))
        >>> send_verification_email("user@qq.com", code)

    Note:
        - 需要设置环境变量 SENDER_EMAIL（发件人邮箱）和 SMTP（授权码）
        - 需要在 QQ 邮箱设置中开启 SMTP 服务并获取授权码
        - Logo 图片路径: config/logo.ico，如果不存在会跳过附加图片
    """
    html = _load_template("verify_code")
    html = html.replace("{verification_code}", verification_num)
    html = _replace_common(html)
    return _build_and_send(email, "验证码", html)


# ============================================================
# 2. 密码重置邮件
# ============================================================

def send_password_reset_email(
    email: str,
    user_name: str,
    reset_link: str,
    expire_hours: int,
    ip: str,
    os_browser: str
) -> None:
    """
    发送密码重置邮件

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        reset_link: 密码重置链接
        expire_hours: 链接有效小时数
        ip: 发起请求的 IP 地址
        os_browser: 操作系统/浏览器信息

    Example:
        >>> send_password_reset_email(
        ...     "user@qq.com", "张三",
        ...     "https://example.com/reset?token=xxx", 2,
        ...     "192.168.1.1", "Windows 10 / Chrome 120"
        ... )
    """
    html = _load_template("password_reset")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{reset_link}", reset_link)
    html = html.replace("{expire_hours}", str(expire_hours))
    html = html.replace("{ip}", ip)
    html = html.replace("{os_browser}", os_browser)
    html = _replace_common(html)
    return _build_and_send(email, "密码重置", html)


# ============================================================
# 3. 密码修改通知邮件
# ============================================================

def send_password_changed_email(
    email: str,
    user_name: str,
    change_time: str,
    ip: str,
    device: str
) -> None:
    """
    发送密码修改通知邮件（纯通知，无操作）

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        change_time: 密码修改时间，如 "2025-01-15 14:30:00"
        ip: 操作 IP 地址
        device: 操作设备信息

    Example:
        >>> send_password_changed_email(
        ...     "user@qq.com", "张三",
        ...     "2025-01-15 14:30:00", "192.168.1.1", "iPhone 15 / iOS 18"
        ... )
    """
    html = _load_template("password_changed")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{change_time}", change_time)
    html = html.replace("{ip}", ip)
    html = html.replace("{device}", device)
    html = _replace_common(html)
    return _build_and_send(email, "密码修改通知", html)


# ============================================================
# 4. 新设备/异地登录提醒邮件
# ============================================================

def send_login_alert_email(
    email: str,
    user_name: str,
    login_time: str,
    location: str,
    ip: str,
    device: str,
    review_link: str
) -> None:
    """
    发送新设备/异地登录提醒邮件（警示型）

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        login_time: 登录时间
        location: 登录地点，如 "广东·广州"
        ip: 登录 IP 地址
        device: 设备信息
        review_link: 查看登录记录的链接

    Example:
        >>> send_login_alert_email(
        ...     "user@qq.com", "张三",
        ...     "2025-01-15 03:45:00", "广东·广州",
        ...     "113.108.xxx.xxx", "Chrome / Android 14",
        ...     "https://example.com/account/security"
        ... )
    """
    html = _load_template("login_alert")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{login_time}", login_time)
    html = html.replace("{location}", location)
    html = html.replace("{ip}", ip)
    html = html.replace("{device}", device)
    html = html.replace("{review_link}", review_link)
    html = _replace_common(html)
    return _build_and_send(email, "安全提醒 - 新设备登录", html)


# ============================================================
# 5. 邮箱变更确认邮件
# ============================================================

def send_email_change_email(
    email: str,
    user_name: str,
    old_email: str,
    new_email: str,
    cancel_link: str
) -> None:
    """
    发送邮箱变更确认邮件（发送到旧邮箱，防劫持）

    Args:
        email: 收件人邮箱地址（旧邮箱）
        user_name: 用户名称
        old_email: 当前（旧）邮箱地址
        new_email: 新邮箱地址
        cancel_link: 取消变更的链接

    Example:
        >>> send_email_change_email(
        ...     "old@qq.com", "张三",
        ...     "old@qq.com", "new@qq.com",
        ...     "https://example.com/account/cancel-email-change?token=xxx"
        ... )
    """
    html = _load_template("email_change")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{old_email}", old_email)
    html = html.replace("{new_email}", new_email)
    html = html.replace("{cancel_link}", cancel_link)
    html = _replace_common(html)
    return _build_and_send(email, "邮箱变更确认", html)


# ============================================================
# 6. 订单确认邮件
# ============================================================

def send_order_confirm_email(
    email: str,
    user_name: str,
    order_id: str,
    order_time: str,
    items: List[dict],
    total: str,
    pay_method: str,
    order_url: str
) -> None:
    """
    发送订单确认邮件（下单/支付成功）

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        order_id: 订单编号
        order_time: 下单时间
        items: 商品列表，每个元素为 dict，格式:
              {"name": "商品名称", "price": "单价", "quantity": "数量"}
        total: 订单总金额，如 "299.00"
        pay_method: 支付方式，如 "微信支付"
        order_url: 查看订单详情的链接

    Example:
        >>> items = [
        ...     {"name": "无线蓝牙耳机", "price": "199.00", "quantity": "1"},
        ...     {"name": "耳机收纳盒", "price": "29.00", "quantity": "2"},
        ... ]
        >>> send_order_confirm_email(
        ...     "user@qq.com", "张三",
        ...     "ORD20250115001", "2025-01-15 14:30:00",
        ...     items, "257.00", "微信支付",
        ...     "https://example.com/orders/ORD20250115001"
        ... )
    """
    # 构建商品列表 HTML
    items_rows = ""
    for item in items:
        items_rows += f"""
            <tr>
                <td style="padding:8px 0; color:#d0c4ff; font-size:13px; border-bottom:1px solid #3f2e75;">
                    {item['name']}
                    <span style="color:#a89cff;">× {item['quantity']}</span>
                    <span style="float:right; color:#ffffff;">¥{item['price']}</span>
                </td>
            </tr>"""

    html = _load_template("order_confirm")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{order_id}", order_id)
    html = html.replace("{order_time}", order_time)
    html = html.replace("{items_html}", items_rows)
    html = html.replace("{total}", total)
    html = html.replace("{pay_method}", pay_method)
    html = html.replace("{order_url}", order_url)
    html = _replace_common(html)
    return _build_and_send(email, f"订单确认 - {order_id}", html)


# ============================================================
# 7. 物流发货通知邮件
# ============================================================

def send_ship_notify_email(
    email: str,
    user_name: str,
    order_id: str,
    tracking_no: str,
    tracking_url: str,
    carrier: str,
    address: str
) -> None:
    """
    发送物流发货通知邮件

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        order_id: 订单编号
        tracking_no: 快递单号
        tracking_url: 物流查询链接
        carrier: 快递公司名称，如 "顺丰速运"
        address: 收货地址

    Example:
        >>> send_ship_notify_email(
        ...     "user@qq.com", "张三",
        ...     "ORD20250115001", "SF1234567890",
        ...     "https://www.sf-express.com/track?no=SF1234567890",
        ...     "顺丰速运", "广东省广州市天河区xxx路xxx号"
        ... )
    """
    html = _load_template("ship_notify")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{order_id}", order_id)
    html = html.replace("{tracking_no}", tracking_no)
    html = html.replace("{tracking_url}", tracking_url)
    html = html.replace("{carrier}", carrier)
    html = html.replace("{address}", address)
    html = _replace_common(html)
    return _build_and_send(email, f"您的包裹已发货 - {order_id}", html)


# ============================================================
# 8. 退款进度通知邮件
# ============================================================

def send_refund_status_email(
    email: str,
    user_name: str,
    order_id: str,
    refund_amount: str,
    status: str,
    reason: str
) -> None:
    """
    发送退款进度通知邮件

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        order_id: 订单编号
        refund_amount: 退款金额，如 "199.00"
        status: 退款状态，如 "已退款"、"审核中"、"已拒绝"
        reason: 退款原因

    Example:
        >>> send_refund_status_email(
        ...     "user@qq.com", "张三",
        ...     "ORD20250115001", "199.00",
        ...     "已退款", "商品与描述不符"
        ... )
    """
    html = _load_template("refund_status")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{order_id}", order_id)
    html = html.replace("{refund_amount}", refund_amount)
    html = html.replace("{status}", status)
    html = html.replace("{reason}", reason)
    html = _replace_common(html)
    return _build_and_send(email, f"退款进度通知 - {order_id}", html)


# ============================================================
# 9. 注册欢迎邮件
# ============================================================

def send_account_welcome_email(
    email: str,
    user_name: str,
    onboarding_steps: List[str],
    verify_link: Optional[str] = None
) -> None:
    """
    发送注册欢迎邮件

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        onboarding_steps: 入门步骤列表，如 ["完善个人资料", "绑定手机号", "浏览推荐内容"]
        verify_link: 邮箱验证链接（可选），为空则不显示验证按钮

    Example:
        >>> steps = ["完善个人资料", "绑定手机号", "浏览推荐内容"]
        >>> send_account_welcome_email(
        ...     "user@qq.com", "张三",
        ...     steps,
        ...     verify_link="https://example.com/verify?token=xxx"
        ... )
    """
    # 构建入门步骤 HTML
    steps_html = ""
    for i, step in enumerate(onboarding_steps, start=1):
        steps_html += f'<p style="color:#a89cff; font-size:13px; margin:0 0 5px 0;">{i}. <strong style="color:#ffffff;">{step}</strong></p>'

    # 构建可选的验证按钮 HTML
    verify_button_html = ""
    if verify_link:
        verify_button_html = f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:30px;">
            <tr>
                <td align="center">
                    <a href="{verify_link}" style="display:inline-block; background:#7b6cd1; color:#ffffff; font-size:16px; font-weight:bold; text-decoration:none; padding:14px 40px; border-radius:10px; border:2px solid #9b8fd1;">验证邮箱 →</a>
                </td>
            </tr>
        </table>"""

    html = _load_template("account_welcome")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{onboarding_steps_html}", steps_html)
    html = html.replace("{verify_button_html}", verify_button_html)
    html = _replace_common(html)
    return _build_and_send(email, f"欢迎加入 {os.getenv('APP_NAME', '')}", html)


# ============================================================
# 10. 促销/优惠券邮件
# ============================================================

def send_promo_batch_email(
    email: str,
    user_name: str,
    event_title: str,
    discount_desc: str,
    coupon_code: str,
    valid_until: str,
    goods: List[dict],
    banner_url: str,
    unsubscribe_url: str
) -> None:
    """
    发送促销/优惠券邮件（营销类，需退订链接）

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        event_title: 活动标题，如 "双十二年终大促"
        discount_desc: 优惠描述，如 "全场满200减30，精选好物低至5折！"
        coupon_code: 优惠券码
        valid_until: 有效期截止日期，如 "2025-12-31"
        goods: 推荐商品列表，每个元素为 dict，格式:
              {"name": "商品名称", "price": "价格", "image_url": "商品图片链接（可选）"}
        banner_url: 活动 banner 图片链接
        unsubscribe_url: 退订链接

    Example:
        >>> goods = [
        ...     {"name": "冬季羽绒服", "price": "¥399"},
        ...     {"name": "保暖围巾", "price": "¥59"},
        ... ]
        >>> send_promo_batch_email(
        ...     "user@qq.com", "张三",
        ...     "双十二年终大促", "全场满200减30！",
        ...     "WINTER2025", "2025-12-31",
        ...     goods,
        ...     "https://example.com/banner/winter-sale.jpg",
        ...     "https://example.com/unsubscribe?uid=xxx"
        ... )
    """
    # 构建商品列表 HTML
    goods_html = ""
    for item in goods:
        img_tag = ""
        if item.get("image_url"):
            img_tag = f'<img src="{item["image_url"]}" width="60" style="display:inline-block; vertical-align:middle; border-radius:8px; margin-right:10px;">'
        goods_html += f"""
            <tr>
                <td style="padding:8px 0; border-bottom:1px solid #3f2e75;">
                    {img_tag}
                    <span style="color:#d0c4ff; font-size:13px;">{item['name']}</span>
                    <span style="float:right; color:#e74c3c; font-weight:bold; font-size:14px;">{item['price']}</span>
                </td>
            </tr>"""

    html = _load_template("promo_batch")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{event_title}", event_title)
    html = html.replace("{discount_desc}", discount_desc)
    html = html.replace("{coupon_code}", coupon_code)
    html = html.replace("{valid_until}", valid_until)
    html = html.replace("{goods_html}", goods_html)
    html = html.replace("{banner_url}", banner_url)
    html = html.replace("{unsubscribe_url}", unsubscribe_url)
    html = _replace_common(html)
    return _build_and_send(email, f"🔥 {event_title} - 限时优惠", html)


# ============================================================
# 11. 周刊/资讯邮件
# ============================================================

def send_newsletter_email(
    email: str,
    user_name: str,
    subject: str,
    articles: List[dict],
    unsubscribe_url: str
) -> None:
    """
    发送周刊/资讯邮件（内容类，需退订链接）

    Args:
        email: 收件人邮箱地址
        user_name: 用户名称
        subject: 周刊主题，如 "AI 前沿周报 #42"
        articles: 文章列表，每个元素为 dict，格式:
                 {"title": "文章标题", "summary": "摘要", "link": "文章链接"}
        unsubscribe_url: 退订链接

    Example:
        >>> articles = [
        ...     {"title": "2025 AI 十大趋势", "summary": "深度解读今年AI领域的重大变革...", "link": "https://example.com/p/ai-trends"},
        ...     {"title": "FastAPI 最佳实践", "summary": "从项目结构到性能优化的一站式指南...", "link": "https://example.com/p/fastapi"},
        ... ]
        >>> send_newsletter_email(
        ...     "user@qq.com", "张三",
        ...     "AI 前沿周报 #42", articles,
        ...     "https://example.com/unsubscribe?uid=xxx"
        ... )
    """
    # 构建文章列表 HTML
    articles_html = ""
    for article in articles:
        articles_html += f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#1f1547; border:1px solid #3f2e75; border-radius:12px; margin-bottom:15px;">
            <tr>
                <td style="padding:20px 25px; text-align:left;">
                    <a href="{article['link']}" style="color:#ffffff; font-size:16px; font-weight:bold; text-decoration:none; display:block; margin:0 0 8px 0;">
                        📄 {article['title']}
                    </a>
                    <p style="color:#a89cff; font-size:13px; line-height:1.6; margin:0 0 12px 0;">
                        {article['summary']}
                    </p>
                    <a href="{article['link']}" style="color:#7b6cd1; font-size:13px; text-decoration:none;">阅读全文 →</a>
                </td>
            </tr>
        </table>"""

    html = _load_template("newsletter")
    html = html.replace("{user_name}", user_name)
    html = html.replace("{subject}", subject)
    html = html.replace("{articles_html}", articles_html)
    html = html.replace("{unsubscribe_url}", unsubscribe_url)
    html = _replace_common(html)
    return _build_and_send(email, f"📰 {subject}", html)


# ============================================================
# 测试代码
# ============================================================

if __name__ == '__main__':
    # 添加邮箱的环境变量
    os.environ['SENDER_EMAIL'] = "自己的QQ邮箱"
    # 添加授权码的环境变量
    os.environ['SMTP'] = "自己去QQ邮箱里找"
    # 发送邮件
    send_verification_email("接收者的邮箱(对面)", ''.join(random.choices('0123456789', k=6)))
