"""main.py
邮件批量发送系统 — 程序主入口
"""
# 内置库
import webbrowser
from datetime import datetime
from contextlib import asynccontextmanager
# 三方库
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List
from fastapi.responses import FileResponse
# 自己的模块
from logger import info
from utils.config_manager import ConfigManager
from utils.path_utils import get_root
# 邮件系统模块
from utils.email_task_db import (
    init_db, insert_tasks_batch, get_all_tasks, get_task_by_id,
    delete_task, delete_tasks_batch, delete_tasks_by_status,
    get_task_count, get_template_definitions, reset_failed_tasks, reset_task_to_pending,
)
from utils.email_dispatcher import (
    send_due_emails, send_single_task, start_scheduler, stop_scheduler,
)
from utils.qrcode_manager import QRCodeManager, get_local_ip
print(get_root())
"""初始化"""
# 是否为开发模式
debug = False
# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager(debug=debug)
info("日志模块加载完成，全局异常捕获开启")
# 层叠覆盖原来的配置
config_manager.config_override()
info("层叠覆盖原来的配置完成")
# 协议
PROTOCOL: str = config_manager.config_data.server.protocol
# 主机号
HOST: str = config_manager.config_data.server.host
# 端口号
PORT: int = config_manager.config_data.server.port
info(f"服务器配置，协议：{PROTOCOL}，主机：{HOST}，端口：{PORT}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 打印服务器信息并打开浏览器
    if HOST == "0.0.0.0":
        info(f"浏览器请访问：{PROTOCOL}://localhost:{PORT}")
        webbrowser.open(f"{PROTOCOL}://localhost:{PORT}")  # 打开用户本地浏览器
        QRCodeManager().create_qrcode(f"{PROTOCOL}://{get_local_ip()}:{PORT}")  # 创建二维码
    else:
        info(f"浏览器请访问：{PROTOCOL}://{HOST}:{PORT}")
        webbrowser.open(f"{PROTOCOL}://{HOST}:{PORT}")  # 打开用户本地浏览器
    # ── 启动阶段 ──
    init_db()
    info("邮件任务数据库初始化完成")
    # 发送所有到期邮件（启动时立即执行一次）
    send_due_emails()
    # 启动后台定时调度器（每 60 秒扫描一次到期任务）
    start_scheduler(interval_seconds=60)

    yield

    # ── 关闭阶段 ──
    stop_scheduler()
    info("邮件调度器已停止")


# 创建 FastAPI 实例
app = FastAPI(lifespan=lifespan)

# ============================================================================
#  邮件批量发送系统 API
# ============================================================================

@app.get("/")
async def email_ui():
    """邮件批量发送管理界面"""
    html_path = get_root() / "templates" / "web_ui" / "index" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 图标
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(get_root() / "config" / "logo.ico")

@app.get("/api/email-tasks/templates")
async def api_get_templates():
    """获取所有支持的邮件模板定义（含变量字段信息）"""
    return JSONResponse(content={
        "code": 200,
        "msg": "success",
        "data": get_template_definitions(),
    })


@app.get("/api/email-tasks")
async def api_get_tasks(status: str = ""):
    """获取所有邮件任务列表"""
    tasks = get_all_tasks(status=status if status else None)
    return JSONResponse(content={
        "code": 200,
        "msg": "success",
        "data": {
            "tasks": tasks,
            "total": len(tasks),
        }
    })


@app.post("/api/email-tasks")
async def api_create_tasks(request: Request):
    """批量创建邮件任务

    请求体 JSON:
    {
        "template_code": "VERIFY_CODE",
        "template_vars": {"verification_code": "123456"},
        "emails": ["user1@qq.com", "user2@qq.com"],
        "send_time": "2025-01-15T14:30:00"  // 可选，默认为当前时间（立即发送）
    }
    """
    body = await request.json()
    template_code = body.get("template_code", "")
    template_vars = body.get("template_vars", {})
    emails = body.get("emails", [])
    send_time = body.get("send_time") or datetime.now().isoformat()

    if not template_code:
        return JSONResponse(status_code=400, content={"code": 400, "msg": "请选择模板类型", "data": None})
    if not emails:
        return JSONResponse(status_code=400, content={"code": 400, "msg": "请填写收件人邮箱", "data": None})

    # 使用 Pydantic EmailStr 逐条校验
    invalid_emails = []
    for email in emails:
        try:
            EmailStr._validate(email.strip())
        except (ValueError, Exception):
            invalid_emails.append(email)
    if invalid_emails:
        return JSONResponse(status_code=400, content={
            "code": 400,
            "msg": f"以下邮箱格式不合法: {', '.join(invalid_emails)}",
            "data": {"invalid_emails": invalid_emails},
        })

    tasks = [
        {"user_email": e.strip(), "send_time": send_time, "template_code": template_code, "template_vars": template_vars}
        for e in emails
    ]
    ids = insert_tasks_batch(tasks)
    info(f"批量创建 {len(ids)} 个邮件任务: {template_code} -> {emails}")

    return JSONResponse(content={
        "code": 200,
        "msg": f"成功创建 {len(ids)} 个邮件任务",
        "data": {"ids": ids, "count": len(ids)},
    })


@app.delete("/api/email-tasks/{task_id}")
async def api_delete_task(task_id: int):
    """删除指定邮件任务"""
    ok = delete_task(task_id)
    if not ok:
        return JSONResponse(status_code=404, content={"code": 404, "msg": f"任务 #{task_id} 不存在", "data": None})
    return JSONResponse(content={"code": 200, "msg": f"任务 #{task_id} 已删除", "data": None})


@app.post("/api/email-tasks/{task_id}/send")
async def api_send_task_now(task_id: int):
    """立即发送指定任务（忽略定时）"""
    ok = send_single_task(task_id)
    if not ok:
        return JSONResponse(status_code=500, content={"code": 500, "msg": f"任务 #{task_id} 发送失败", "data": None})
    return JSONResponse(content={"code": 200, "msg": f"任务 #{task_id} 发送成功", "data": None})


@app.post("/api/email-tasks/send-due")
async def api_send_due_tasks():
    """立即发送所有到期未发的任务"""
    count = send_due_emails()
    return JSONResponse(content={"code": 200, "msg": f"已发送 {count} 封到期邮件", "data": {"sent": count}})


@app.post("/api/email-tasks/send-all-pending")
async def api_send_all_pending():
    """一键发送所有待发送任务（忽略定时）"""
    tasks = get_all_tasks("pending")
    if not tasks:
        return JSONResponse(content={"code": 200, "msg": "没有待发送任务", "data": {"sent": 0}})
    success = 0
    for t in tasks:
        ok = send_single_task(t["id"])
        if ok:
            success += 1
    return JSONResponse(content={"code": 200, "msg": f"已发送 {success}/{len(tasks)} 封", "data": {"sent": success, "total": len(tasks)}})


@app.post("/api/email-tasks/resend-failed")
async def api_resend_failed():
    """重试所有失败任务"""
    count = reset_failed_tasks()
    if count == 0:
        return JSONResponse(content={"code": 200, "msg": "没有失败任务需要重试", "data": {"reset": 0}})
    # 立即发送这些刚重置的任务
    sent = send_due_emails()
    return JSONResponse(content={"code": 200, "msg": f"已重置 {count} 个失败任务，成功发送 {sent} 个", "data": {"reset": count, "sent": sent}})


@app.post("/api/email-tasks/{task_id}/retry")
async def api_retry_task(task_id: int):
    """重试单个失败任务"""
    task = get_task_by_id(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"code": 404, "msg": f"任务 #{task_id} 不存在", "data": None})
    if task["status"] != "failed":
        return JSONResponse(status_code=400, content={"code": 400, "msg": "只能重试失败的任务", "data": None})
    reset_task_to_pending(task_id)
    ok = send_single_task(task_id)
    return JSONResponse(content={"code": 200 if ok else 500, "msg": f"任务 #{task_id} 重试{'成功' if ok else '失败'}", "data": None})


@app.delete("/api/email-tasks/batch")
async def api_delete_tasks_batch(request: Request):
    """批量删除任务"""
    body = await request.json()
    ids = body.get("ids", [])
    if not ids:
        return JSONResponse(status_code=400, content={"code": 400, "msg": "请提供要删除的任务 ID 列表", "data": None})
    count = delete_tasks_batch(ids)
    return JSONResponse(content={"code": 200, "msg": f"已删除 {count} 个任务", "data": {"deleted": count}})


@app.delete("/api/email-tasks/clean/completed")
async def api_clean_completed():
    """清空所有已完成（已发送）的任务"""
    count = delete_tasks_by_status("sent")
    return JSONResponse(content={"code": 200, "msg": f"已清空 {count} 条已完成记录", "data": {"deleted": count}})


@app.get("/api/email-tasks/stats")
async def api_get_stats():
    """获取任务统计信息"""
    total = get_task_count()
    pending = get_task_count("pending")
    sent = get_task_count("sent")
    failed = get_task_count("failed")
    return JSONResponse(content={
        "code": 200,
        "msg": "success",
        "data": {"total": total, "pending": pending, "sent": sent, "failed": failed},
    })


# 静态文件挂载
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")


# ============================================================================
#  邮箱校验 API
# ============================================================================

class EmailsValidateRequest(BaseModel):
    """邮箱批量校验请求体"""
    emails: List[str]


@app.post("/api/email-tasks/validate-emails")
async def api_validate_emails(request: EmailsValidateRequest):
    """批量校验邮箱格式（使用 Pydantic EmailStr）

    逐条校验每个邮箱，返回每条的结果，精确定位错误行。
    """
    results = []
    for idx, email in enumerate(request.emails):
        email = email.strip()
        if not email:
            results.append({"line": idx + 1, "email": "(空)", "valid": False, "error": "邮箱为空"})
            continue
        try:
            # Pydantic EmailStr 严格校验
            EmailStr._validate(email)
            results.append({"line": idx + 1, "email": email, "valid": True, "error": None})
        except ValueError:
            results.append({"line": idx + 1, "email": email, "valid": False, "error": "邮箱格式不合法"})
        except Exception:
            results.append({"line": idx + 1, "email": email, "valid": False, "error": "邮箱校验异常"})

    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = len(results) - valid_count
    
    return JSONResponse(content={
        "code": 200,
        "msg": "success",
        "data": {
            "total": len(results),
            "valid_count": valid_count,
            "invalid_count": invalid_count,
            "results": results,
        }
    })


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
