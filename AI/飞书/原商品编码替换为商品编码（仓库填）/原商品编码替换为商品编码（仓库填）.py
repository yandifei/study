# -*- coding: utf-8 -*-
import sys
import time
import threading
import logging
import re
import ctypes
import ctypes.wintypes
from pathlib import Path

import keyboard
import pyperclip
import pandas as pd
import pystray
from PIL import Image, ImageDraw

# ======================== 用户配置区 ========================
EXCEL_PATH = "data.xlsx"             # Excel 文件路径（推荐绝对路径或相对路径）
SHEET_NAME = None                     # 工作表名称，None 表示使用第一个
PATTERN = r'^smartband\d+pro'        # 正则表达式，用于格式校验（请按实际修改）
REPLACE_FAIL_MSG = "没有找到该数据，请更新“Excel文件”或手动查找"
DELAY = 0.1                           # 延迟秒数，等待系统完成复制

COL_ORIGINAL = "原商品编码"            # Excel 中“原商品编码”列的列名
COL_TARGET = "商品编码（仓库填）"      # Excel 中目标列列名
# ===========================================================

# 日志配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 全局映射字典
mapping = {}


def check_single_instance():
    """使用互斥体检查是否已有实例运行"""
    mutex_name = "Global\\ClipboardAutoMapperMutex"
    try:
        handle = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
        if handle:
            last_error = ctypes.windll.kernel32.GetLastError()
            if last_error == 183:  # ERROR_ALREADY_EXISTS
                return False
            return True
        return False
    except Exception as e:
        logger.error(f"检查单实例失败: {e}")
        return True  # 发生异常时继续运行


def load_excel():
    """加载 Excel 并构建映射字典"""
    global mapping
    try:
        if not Path(EXCEL_PATH).exists():
            logger.error(f"Excel 文件不存在: {EXCEL_PATH}")
            return False

        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, dtype=str)
        if COL_ORIGINAL not in df.columns:
            logger.error(f"Excel 缺少列: {COL_ORIGINAL}")
            return False
        if COL_TARGET not in df.columns:
            logger.error(f"Excel 缺少列: {COL_TARGET}")
            return False

        df = df.dropna(subset=[COL_ORIGINAL])
        mapping = dict(zip(df[COL_ORIGINAL].astype(str),
                           df[COL_TARGET].astype(str)))
        logger.info(f"成功加载 {len(mapping)} 条映射记录")
        return True
    except Exception as e:
        logger.error(f"读取 Excel 失败: {e}")
        return False


def validate_format(text):
    """格式校验（正则匹配）"""
    if not text:
        return False
    return re.match(PATTERN, text) is not None


def process_clipboard():
    """处理剪贴板内容（在独立线程中运行）"""
    time.sleep(DELAY)  # 等待系统将内容写入剪贴板
    try:
        text = pyperclip.paste()
        if not text:
            return
        logger.debug(f"读取到剪贴板: {text[:50]}...")

        if not validate_format(text):
            logger.debug("格式不匹配，忽略")
            return

        if text in mapping:
            new_text = mapping[text]
            pyperclip.copy(new_text)
            logger.info(f"替换成功: {text} -> {new_text}")
        else:
            pyperclip.copy(REPLACE_FAIL_MSG)
            logger.warning(f"未找到映射: {text}")
    except Exception as e:
        logger.error(f"处理剪贴板时出错: {e}")


def on_ctrl_c():
    """Ctrl+C 热键回调（启动新线程处理）"""
    threading.Thread(target=process_clipboard, daemon=True).start()


def create_icon():
    """生成托盘图标（使用 PIL 绘制）"""
    size = 64
    image = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, size-1, size-1], outline='black', width=2)
    draw.text((10, 20), "CM", fill='black')
    return image


def quit_app(icon, item):
    """退出程序"""
    icon.stop()
    sys.exit(0)


def reload_excel(icon, item):
    """重新加载 Excel（菜单项）"""
    success = load_excel()
    if success:
        logger.info("重新加载 Excel 成功")
    else:
        logger.error("重新加载 Excel 失败")


def main():
    # 单实例检查
    if not check_single_instance():
        logger.warning("程序已在运行，退出")
        try:
            ctypes.windll.user32.MessageBoxW(0, "程序已在运行！", "提示", 0)
        except:
            pass
        sys.exit(0)

    # 加载 Excel
    if not load_excel():
        logger.error("加载 Excel 失败，程序退出")
        try:
            ctypes.windll.user32.MessageBoxW(
                0, f"加载 Excel 失败，请检查文件路径：{EXCEL_PATH}", "错误", 0
            )
        except:
            pass
        sys.exit(1)

    # 注册全局热键
    try:
        keyboard.add_hotkey('ctrl+c', on_ctrl_c)
        logger.info("已注册 Ctrl+C 热键监听")
    except Exception as e:
        logger.error(f"注册热键失败，请以管理员身份运行: {e}")
        try:
            ctypes.windll.user32.MessageBoxW(
                0, "注册热键失败，请以管理员身份运行！", "错误", 0
            )
        except:
            pass
        sys.exit(1)

    # 创建托盘图标
    icon_image = create_icon()
    menu = pystray.Menu(
        pystray.MenuItem("重新加载 Excel", reload_excel),
        pystray.MenuItem("退出", quit_app)
    )
    icon = pystray.Icon("clipboard_mapper", icon_image,
                        "剪贴板自动映射助手", menu)

    # 启动托盘（阻塞主线程）
    icon.run()


if __name__ == "__main__":
    main()