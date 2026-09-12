import re
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

import pandas as pd
import keyboard
import pyperclip


# 打包路径处理
def get_root() -> Path:
    """获取项目根目录（当前文件的上两级目录）"""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS).resolve().parent
    return Path(__file__).resolve().parent

# ===== 配置区域 =====
EXCEL_PATH  = rf"{get_root()}/data.xlsx"
SHEET_NAME  = 0
COL_ORIGINAL = "原商品编码"
COL_TARGET   = "商品编码（仓库填）"
PATTERN      = r'^[A-Za-z0-9\-_]+$'
FAIL_TEXT    = '没有找到该数据，请更新“Excel文件”或手动查找'

# ===== 新增日志配置 =====
LOG_FILE    = "日志记录.txt"      # 日志文件路径
LOG_DELIM   = "\t"                         # 字段分隔符（制表符）
# =========================

# 全局变量
mapping = {}
lock = threading.Lock()
log_lock = threading.Lock()   # 专门用于日志写入的锁

def write_log(original: str, replaced: str, status: str):
    """
    写入一条日志记录
    :param original: 原始剪贴板内容
    :param replaced: 替换后的内容
    :param status: 状态，如 '成功' 或 '失败'
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 精确到毫秒
    # 转义字段中的制表符和换行符，防止破坏格式
    def escape_field(text: str) -> str:
        return text.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    log_line = f"{timestamp}{LOG_DELIM}{escape_field(original)}{LOG_DELIM}{escape_field(replaced)}{LOG_DELIM}{status}\n"
    print(log_line)
    with log_lock:
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            print(f"写入日志失败：{e}")

def load_mapping():
    """加载 Excel 并构建查找字典"""
    global mapping
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, dtype=str)
        df.columns = df.columns.str.strip()
        if COL_ORIGINAL not in df.columns or COL_TARGET not in df.columns:
            print(f"错误：Excel 中未找到列 '{COL_ORIGINAL}' 或 '{COL_TARGET}'")
            return False
        df[COL_ORIGINAL] = df[COL_ORIGINAL].dropna().str.strip()
        df[COL_TARGET] = df[COL_TARGET].fillna('').str.strip()
        mapping = dict(zip(df[COL_ORIGINAL], df[COL_TARGET]))
        print(f"映射表加载成功，共 {len(mapping)} 条记录")
        return True
    except Exception as e:
        print(f"加载 Excel 失败：{e}")
        return False

def on_ctrl_c():
    """Ctrl+C 回调：延迟读取剪贴板 → 正则校验 → 查表替换 → 记录日志"""
    time.sleep(0.05)  # 等待系统完成复制
    try:
        original = pyperclip.paste()
    except Exception:
        return

    # 1. 格式预校验
    if not original or not re.fullmatch(PATTERN, original):
        return  # 不符合编码格式，不做任何处理

    # 2. 查表
    with lock:
        target = mapping.get(original)

    # 3. 替换剪贴板并记录日志
    if target:
        pyperclip.copy(target)
        write_log(original, target, "成功")

    else:
        pyperclip.copy(FAIL_TEXT)
        write_log(original, FAIL_TEXT, "失败")


def main():

    if not load_mapping():
        print("按任意键退出...")
        input()
        return

    # 注册 Ctrl+C 热键
    keyboard.add_hotkey('ctrl+c', on_ctrl_c, suppress=False)
    print("程序已启动，按 ESC 键退出。")
    print("按下 Ctrl+C 将自动映射（仅匹配格式的文本）")

    keyboard.wait('esc')
    print("程序已退出")

if __name__ == "__main__":
    main()