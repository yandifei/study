"""email_task_db.py
SQLite 数据库服务层 — 管理邮件发送任务的持久化存储。

提供任务的增删改查，以及批量插入、到期查询等功能。
数据库文件存储在 user_data/email_tasks.db。
"""
import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

from utils.path_utils import get_root, mkdir

# 数据库文件路径
DB_DIR = get_root() / "user_data"
DB_PATH = DB_DIR / "email_tasks.db"

# 线程锁，确保 SQLite 写入操作的线程安全
_db_lock = threading.Lock()


def _ensure_db_dir() -> None:
    """确保 user_data 目录存在"""
    mkdir(DB_DIR)


def _get_connection() -> sqlite3.Connection:
    """获取数据库连接（自动创建目录和表）"""
    _ensure_db_dir()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """初始化数据库表结构（首次运行时自动调用，含向前兼容迁移）"""
    with _db_lock:
        conn = _get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS email_tasks (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email      TEXT    NOT NULL,
                    send_time       TEXT    NOT NULL,
                    template_code   TEXT    NOT NULL,
                    template_vars   TEXT    NOT NULL DEFAULT '{}',
                    status          TEXT    NOT NULL DEFAULT 'pending',
                    error_msg       TEXT,
                    created_at      TEXT    NOT NULL,
                    sent_at         TEXT
                )
            """)
            # 向前兼容：旧表可能没有 error_msg 列
            try:
                conn.execute("ALTER TABLE email_tasks ADD COLUMN error_msg TEXT")
            except:
                pass
            conn.commit()
        finally:
            conn.close()


def insert_task(
    user_email: str,
    send_time: str,
    template_code: str,
    template_vars: dict,
) -> int:
    """插入一条邮件任务

    Args:
        user_email: 收件人邮箱
        send_time: 计划发送时间（ISO 格式字符串）
        template_code: 模板代码，如 VERIFY_CODE
        template_vars: 模板变量字典

    Returns:
        新插入任务的自增 ID
    """
    with _db_lock:
        conn = _get_connection()
        try:
            cursor = conn.execute(
                """INSERT INTO email_tasks (user_email, send_time, template_code, template_vars, status, created_at)
                   VALUES (?, ?, ?, ?, 'pending', ?)""",
                (user_email, send_time, template_code, json.dumps(template_vars, ensure_ascii=False), datetime.now().isoformat())
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()


def insert_tasks_batch(tasks: list[dict]) -> list[int]:
    """批量插入邮件任务

    Args:
        tasks: 任务列表，每个元素为 dict:
               {"user_email": str, "send_time": str, "template_code": str, "template_vars": dict}

    Returns:
        新插入任务的 ID 列表
    """
    with _db_lock:
        conn = _get_connection()
        try:
            now = datetime.now().isoformat()
            ids = []
            for task in tasks:
                cursor = conn.execute(
                    """INSERT INTO email_tasks (user_email, send_time, template_code, template_vars, status, created_at)
                       VALUES (?, ?, ?, ?, 'pending', ?)""",
                    (task["user_email"], task["send_time"], task["template_code"],
                     json.dumps(task.get("template_vars", {}), ensure_ascii=False), now)
                )
                ids.append(cursor.lastrowid)
            conn.commit()
            return ids
        finally:
            conn.close()


def get_due_tasks() -> list[dict]:
    """查询所有到期未发送的任务（send_time <= 当前时间 且 status='pending'）

    Returns:
        到期任务列表
    """
    conn = _get_connection()
    try:
        now = datetime.now().isoformat()
        rows = conn.execute(
            """SELECT * FROM email_tasks
               WHERE status = 'pending' AND send_time <= ?
               ORDER BY send_time ASC""",
            (now,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_all_tasks(status: Optional[str] = None) -> list[dict]:
    """查询所有任务（可按状态过滤）

    Args:
        status: 可选的状态过滤条件

    Returns:
        任务列表
    """
    conn = _get_connection()
    try:
        if status:
            rows = conn.execute(
                "SELECT * FROM email_tasks WHERE status = ? ORDER BY created_at DESC",
                (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM email_tasks ORDER BY created_at DESC"
            ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_task_by_id(task_id: int) -> Optional[dict]:
    """根据 ID 查询单个任务"""
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM email_tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def mark_task_sent(task_id: int) -> None:
    """将任务标记为已发送"""
    with _db_lock:
        conn = _get_connection()
        try:
            conn.execute(
                "UPDATE email_tasks SET status = 'sent', sent_at = ? WHERE id = ?",
                (datetime.now().isoformat(), task_id)
            )
            conn.commit()
        finally:
            conn.close()


def mark_task_failed(task_id: int, error_msg: str = "") -> None:
    """将任务标记为发送失败，同时记录错误信息"""
    with _db_lock:
        conn = _get_connection()
        try:
            conn.execute(
                "UPDATE email_tasks SET status = 'failed', error_msg = ?, sent_at = ? WHERE id = ?",
                (error_msg[:500] if error_msg else "", datetime.now().isoformat(), task_id)
            )
            conn.commit()
        finally:
            conn.close()


def delete_task(task_id: int) -> bool:
    """删除任务

    Returns:
        True 表示删除成功，False 表示任务不存在
    """
    with _db_lock:
        conn = _get_connection()
        try:
            cursor = conn.execute("DELETE FROM email_tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


def get_task_count(status: Optional[str] = None) -> int:
    """获取任务数量（可按状态过滤）"""
    conn = _get_connection()
    try:
        if status:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM email_tasks WHERE status = ?", (status,)
            ).fetchone()
        else:
            row = conn.execute("SELECT COUNT(*) as cnt FROM email_tasks").fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


# ============================================================
# 模板定义（供 API 和 UI 使用）
# ============================================================

TEMPLATE_DEFINITIONS = {
    "VERIFY_CODE": {
        "name": "验证码邮件",
        "description": "邮箱验证、注册验证码、登录验证码",
        "fields": [
            {"key": "verification_code", "label": "验证码", "type": "text", "required": True, "placeholder": "6位数字验证码"},
        ]
    },
    "PASSWORD_RESET": {
        "name": "密码重置",
        "description": "密码重置邮件",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "reset_link", "label": "重置链接", "type": "url", "required": True, "placeholder": "https://example.com/reset?token=xxx"},
            {"key": "expire_hours", "label": "有效期(小时)", "type": "number", "required": True, "placeholder": "2"},
            {"key": "ip", "label": "请求IP", "type": "text", "required": True, "placeholder": "192.168.1.1"},
            {"key": "os_browser", "label": "操作系统/浏览器", "type": "text", "required": True, "placeholder": "Windows 10 / Chrome 120"},
        ]
    },
    "PASSWORD_CHANGED": {
        "name": "密码修改通知",
        "description": "密码修改成功通知（纯通知，无操作）",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "change_time", "label": "修改时间", "type": "text", "required": True, "placeholder": "2025-01-15 14:30:00"},
            {"key": "ip", "label": "操作IP", "type": "text", "required": True, "placeholder": "192.168.1.1"},
            {"key": "device", "label": "操作设备", "type": "text", "required": True, "placeholder": "iPhone 15 / iOS 18"},
        ]
    },
    "LOGIN_ALERT": {
        "name": "登录提醒",
        "description": "新设备/异地登录安全提醒",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "login_time", "label": "登录时间", "type": "text", "required": True, "placeholder": "2025-01-15 03:45:00"},
            {"key": "location", "label": "登录地点", "type": "text", "required": True, "placeholder": "广东·广州"},
            {"key": "ip", "label": "登录IP", "type": "text", "required": True, "placeholder": "113.108.xxx.xxx"},
            {"key": "device", "label": "设备信息", "type": "text", "required": True, "placeholder": "Chrome / Android 14"},
            {"key": "review_link", "label": "查看记录链接", "type": "url", "required": True, "placeholder": "https://example.com/account/security"},
        ]
    },
    "EMAIL_CHANGE": {
        "name": "邮箱变更确认",
        "description": "修改邮箱 — 旧邮箱确认（防劫持）",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "old_email", "label": "旧邮箱", "type": "email", "required": True, "placeholder": "old@example.com"},
            {"key": "new_email", "label": "新邮箱", "type": "email", "required": True, "placeholder": "new@example.com"},
            {"key": "cancel_link", "label": "取消变更链接", "type": "url", "required": True, "placeholder": "https://example.com/cancel?token=xxx"},
        ]
    },
    "ORDER_CONFIRM": {
        "name": "订单确认",
        "description": "下单/支付成功通知",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "order_id", "label": "订单编号", "type": "text", "required": True, "placeholder": "ORD20250115001"},
            {"key": "order_time", "label": "下单时间", "type": "text", "required": True, "placeholder": "2025-01-15 14:30:00"},
            {"key": "items", "label": "商品列表(JSON)", "type": "json", "required": True, "placeholder": '[{"name":"商品A","price":"99.00","quantity":"1"}]'},
            {"key": "total", "label": "订单金额", "type": "text", "required": True, "placeholder": "299.00"},
            {"key": "pay_method", "label": "支付方式", "type": "text", "required": True, "placeholder": "微信支付"},
            {"key": "order_url", "label": "订单详情链接", "type": "url", "required": True, "placeholder": "https://example.com/orders/xxx"},
        ]
    },
    "SHIP_NOTIFY": {
        "name": "物流发货通知",
        "description": "物流发货通知",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "order_id", "label": "订单编号", "type": "text", "required": True, "placeholder": "ORD20250115001"},
            {"key": "tracking_no", "label": "快递单号", "type": "text", "required": True, "placeholder": "SF1234567890"},
            {"key": "tracking_url", "label": "物流查询链接", "type": "url", "required": True, "placeholder": "https://www.sf-express.com/track?no=xxx"},
            {"key": "carrier", "label": "快递公司", "type": "text", "required": True, "placeholder": "顺丰速运"},
            {"key": "address", "label": "收货地址", "type": "text", "required": True, "placeholder": "广东省广州市天河区xxx路xxx号"},
        ]
    },
    "REFUND_STATUS": {
        "name": "退款进度通知",
        "description": "退款状态变更通知",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "order_id", "label": "订单编号", "type": "text", "required": True, "placeholder": "ORD20250115001"},
            {"key": "refund_amount", "label": "退款金额", "type": "text", "required": True, "placeholder": "199.00"},
            {"key": "status", "label": "退款状态", "type": "text", "required": True, "placeholder": "已退款 / 审核中 / 已拒绝"},
            {"key": "reason", "label": "退款原因", "type": "text", "required": True, "placeholder": "商品与描述不符"},
        ]
    },
    "ACCOUNT_WELCOME": {
        "name": "注册欢迎",
        "description": "新用户注册欢迎邮件",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "onboarding_steps", "label": "入门步骤(JSON数组)", "type": "json", "required": True, "placeholder": '["完善个人资料","绑定手机号","浏览推荐内容"]'},
            {"key": "verify_link", "label": "验证链接(可选)", "type": "url", "required": False, "placeholder": "https://example.com/verify?token=xxx（可选）"},
        ]
    },
    "PROMO_BATCH": {
        "name": "促销/优惠券",
        "description": "营销类邮件（需退订）",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "event_title", "label": "活动标题", "type": "text", "required": True, "placeholder": "双十二年终大促"},
            {"key": "discount_desc", "label": "优惠描述", "type": "text", "required": True, "placeholder": "全场满200减30，精选好物低至5折！"},
            {"key": "coupon_code", "label": "优惠券码", "type": "text", "required": True, "placeholder": "WINTER2025"},
            {"key": "valid_until", "label": "有效期至", "type": "text", "required": True, "placeholder": "2025-12-31"},
            {"key": "goods", "label": "商品列表(JSON)", "type": "json", "required": True, "placeholder": '[{"name":"羽绒服","price":"¥399"}]'},
            {"key": "banner_url", "label": "Banner图片链接", "type": "url", "required": True, "placeholder": "https://example.com/banner.jpg"},
            {"key": "unsubscribe_url", "label": "退订链接", "type": "url", "required": True, "placeholder": "https://example.com/unsubscribe?uid=xxx"},
        ]
    },
    "NEWSLETTER": {
        "name": "周刊/资讯",
        "description": "内容类邮件（需退订）",
        "fields": [
            {"key": "user_name", "label": "用户名", "type": "text", "required": True, "placeholder": "收件人姓名"},
            {"key": "subject", "label": "周刊主题", "type": "text", "required": True, "placeholder": "AI 前沿周报 #42"},
            {"key": "articles", "label": "文章列表(JSON)", "type": "json", "required": True, "placeholder": '[{"title":"文章标题","summary":"摘要","link":"https://..."}]'},
            {"key": "unsubscribe_url", "label": "退订链接", "type": "url", "required": True, "placeholder": "https://example.com/unsubscribe?uid=xxx"},
        ]
    },
}


def reset_failed_tasks() -> int:
    """将所有失败任务重置为待发送状态（用于重试）

    Returns:
        重置的任务数量
    """
    with _db_lock:
        conn = _get_connection()
        try:
            cursor = conn.execute(
                "UPDATE email_tasks SET status = 'pending', error_msg = NULL, sent_at = NULL WHERE status = 'failed'"
            )
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()


def reset_task_to_pending(task_id: int) -> bool:
    """将单个任务重置为待发送"""
    with _db_lock:
        conn = _get_connection()
        try:
            cursor = conn.execute(
                "UPDATE email_tasks SET status = 'pending', error_msg = NULL, sent_at = NULL WHERE id = ?",
                (task_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


def delete_tasks_batch(task_ids: list[int]) -> int:
    """批量删除任务

    Returns:
        删除的任务数量
    """
    if not task_ids:
        return 0
    with _db_lock:
        conn = _get_connection()
        try:
            placeholders = ','.join('?' * len(task_ids))
            cursor = conn.execute(
                f"DELETE FROM email_tasks WHERE id IN ({placeholders})",
                task_ids
            )
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()


def delete_tasks_by_status(status: str) -> int:
    """删除指定状态的全部任务

    Returns:
        删除的任务数量
    """
    with _db_lock:
        conn = _get_connection()
        try:
            cursor = conn.execute("DELETE FROM email_tasks WHERE status = ?", (status,))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()


def get_template_definitions() -> dict:
    """获取所有模板定义"""
    return TEMPLATE_DEFINITIONS


def get_template_codes() -> list[str]:
    """获取所有模板代码列表"""
    return list(TEMPLATE_DEFINITIONS.keys())
