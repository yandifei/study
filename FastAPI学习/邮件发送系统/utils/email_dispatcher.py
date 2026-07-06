"""email_dispatcher.py
邮件调度器 — 根据模板代码和变量字典，调用对应的发送函数。
同时提供定时任务扫描和批量发送功能。
"""
import json
import threading
import time
from datetime import datetime
from typing import Optional

from logger import info, warning, error as log_error
from utils.email_task_db import (
    get_due_tasks,
    mark_task_sent,
    mark_task_failed,
    get_task_by_id,
)
from utils.message_util import (
    send_verification_email,
    send_password_reset_email,
    send_password_changed_email,
    send_login_alert_email,
    send_email_change_email,
    send_order_confirm_email,
    send_ship_notify_email,
    send_refund_status_email,
    send_account_welcome_email,
    send_promo_batch_email,
    send_newsletter_email,
)

# 模板代码 → 发送函数 映射表
DISPATCH_MAP = {
    "VERIFY_CODE":      {"fn": send_verification_email,      "arg_map": ["email", "verification_code"]},
    "PASSWORD_RESET":   {"fn": send_password_reset_email,     "arg_map": ["email", "user_name", "reset_link", "expire_hours", "ip", "os_browser"]},
    "PASSWORD_CHANGED": {"fn": send_password_changed_email,   "arg_map": ["email", "user_name", "change_time", "ip", "device"]},
    "LOGIN_ALERT":      {"fn": send_login_alert_email,        "arg_map": ["email", "user_name", "login_time", "location", "ip", "device", "review_link"]},
    "EMAIL_CHANGE":     {"fn": send_email_change_email,       "arg_map": ["email", "user_name", "old_email", "new_email", "cancel_link"]},
    "ORDER_CONFIRM":    {"fn": send_order_confirm_email,      "arg_map": ["email", "user_name", "order_id", "order_time", "items", "total", "pay_method", "order_url"]},
    "SHIP_NOTIFY":      {"fn": send_ship_notify_email,        "arg_map": ["email", "user_name", "order_id", "tracking_no", "tracking_url", "carrier", "address"]},
    "REFUND_STATUS":    {"fn": send_refund_status_email,      "arg_map": ["email", "user_name", "order_id", "refund_amount", "status", "reason"]},
    "ACCOUNT_WELCOME":  {"fn": send_account_welcome_email,    "arg_map": ["email", "user_name", "onboarding_steps", "verify_link"]},
    "PROMO_BATCH":      {"fn": send_promo_batch_email,        "arg_map": ["email", "user_name", "event_title", "discount_desc", "coupon_code", "valid_until", "goods", "banner_url", "unsubscribe_url"]},
    "NEWSLETTER":       {"fn": send_newsletter_email,         "arg_map": ["email", "user_name", "subject", "articles", "unsubscribe_url"]},
}


def dispatch_email(
    email: str,
    template_code: str,
    template_vars: dict,
) -> tuple[bool, str]:
    """根据模板代码分发到对应的发送函数

    Args:
        email: 收件人邮箱
        template_code: 模板代码
        template_vars: 模板变量字典

    Returns:
        (True, "") 表示发送成功，(False, error_msg) 表示失败
    """
    if template_code not in DISPATCH_MAP:
        msg = f"未知的模板代码: {template_code}"
        log_error(msg)
        return False, msg

    entry = DISPATCH_MAP[template_code]
    fn = entry["fn"]
    arg_map = entry["arg_map"]

    # 构建参数列表
    args = []
    for arg_name in arg_map:
        if arg_name == "email":
            args.append(email)
        else:
            val = template_vars.get(arg_name)
            # 对数字类型做转换
            if arg_name == "expire_hours" and isinstance(val, str):
                val = int(val)
            args.append(val)

    try:
        ok = fn(*args)
        if ok is True:
            return True, ""
        elif ok is False:
            return False, "SMTP 发送失败（凭据错误或网络不通）"
        return True, ""
    except Exception as e:
        msg = f"{type(e).__name__}: {str(e)[:200]}"
        log_error(f"邮件发送失败 [{template_code}] -> {email}: {msg}")
        return False, msg


def send_due_emails() -> int:
    """发送所有到期未发的邮件

    Returns:
        成功发送的数量
    """
    tasks = get_due_tasks()
    if not tasks:
        return 0

    info(f"发现 {len(tasks)} 封到期邮件待发送")
    success_count = 0

    for task in tasks:
        task_id = task["id"]
        email = task["user_email"]
        template_code = task["template_code"]

        try:
            template_vars = json.loads(task["template_vars"])
        except json.JSONDecodeError:
            template_vars = {}

        info(f"正在发送 #{task_id}: {email} [{template_code}]")
        ok, err_msg = dispatch_email(email, template_code, template_vars)

        if ok:
            mark_task_sent(task_id)
            success_count += 1
        else:
            mark_task_failed(task_id, err_msg)

    info(f"定时发送完成: {success_count}/{len(tasks)} 成功")
    return success_count


def send_single_task(task_id: int) -> bool:
    """立即发送指定 ID 的任务

    Args:
        task_id: 任务 ID

    Returns:
        True 表示发送成功
    """
    task = get_task_by_id(task_id)
    if not task:
        warning(f"任务 #{task_id} 不存在")
        return False

    email = task["user_email"]
    template_code = task["template_code"]

    try:
        template_vars = json.loads(task["template_vars"])
    except json.JSONDecodeError:
        template_vars = {}

    ok, err_msg = dispatch_email(email, template_code, template_vars)

    if ok:
        mark_task_sent(task_id)
    else:
        mark_task_failed(task_id, err_msg)

    return ok


# ============================================================
# 后台定时扫描线程
# ============================================================

_scheduler_thread: Optional[threading.Thread] = None
_scheduler_stop_event = threading.Event()


def _scheduler_loop(interval_seconds: int = 60) -> None:
    """后台调度循环：每隔 interval_seconds 秒扫描一次到期任务"""
    info(f"邮件定时调度器已启动，扫描间隔 {interval_seconds}s")
    while not _scheduler_stop_event.is_set():
        try:
            send_due_emails()
        except Exception as e:
            log_error(f"定时调度器异常: {e}")
        # 等待间隔（可被 stop 事件中断）
        _scheduler_stop_event.wait(interval_seconds)


def start_scheduler(interval_seconds: int = 60) -> None:
    """启动后台定时调度线程

    Args:
        interval_seconds: 扫描间隔（秒），默认 60
    """
    global _scheduler_thread, _scheduler_stop_event
    if _scheduler_thread is not None and _scheduler_thread.is_alive():
        warning("调度器已在运行中")
        return

    _scheduler_stop_event.clear()
    _scheduler_thread = threading.Thread(
        target=_scheduler_loop,
        args=(interval_seconds,),
        daemon=True,
        name="email-scheduler"
    )
    _scheduler_thread.start()


def stop_scheduler() -> None:
    """停止后台调度线程"""
    global _scheduler_thread, _scheduler_stop_event
    if _scheduler_thread is None:
        return
    _scheduler_stop_event.set()
    _scheduler_thread.join(timeout=5)
    info("邮件定时调度器已停止")
