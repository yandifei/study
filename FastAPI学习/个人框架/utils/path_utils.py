"""path _utils.py
路径工具函数集合（Pythonic 风格）。
使用 pathlib 封装常用路径操作。（需要用到啥我就写啥，毕竟方法名我来定义方便记住）
"""
import sys
from pathlib import Path

def get_root() -> Path:
    """获取项目根目录（当前文件的上两级目录）
    通过解析当前文件（`__file__`）的绝对路径，然后获取其父目录的父目录。
    :return: 项目的根目录 Path 对象。
    """
    # 如果是打包环境，sys 模块会有 _MEIPASS 属性
    if hasattr(sys, '_MEIPASS'):
        # 直接返回打包后的程序包的目录
        return Path(sys._MEIPASS).resolve().parent
    return Path(__file__).resolve().parent.parent

def is_path_exist(path: str | Path) -> bool:
    """判断路径是否存在

    :param path: 待检查的路径字符串。
    :return: 如果路径存在则返回 True，否则返回 False。
    """
    # 假设原代码中的 `str | Path` 主要用来接收 str 类型作为输入
    return Path(path).exists()

def get_parent_path(path: str) -> Path:
    """获取给定路径的父目录路径

    :param path: 目标路径字符串。
    :return: 目标路径的父目录 Path 对象。
    """
    # 假设原代码中的 `str | Path` 主要用来接收 str 类型作为输入
    return Path(path).resolve().parent


def mkdir(path: str | Path) -> Path:
    """递归创建目录

    使用 pathlib 的 mkdir 方法递归创建目录，并确保：
    1. **parents=True**: 自动创建路径中所有不存在的父目录。
    2. **exist_ok=True**: 如果目标目录已存在，不会抛出 FileExistsError 异常。

    :param path: 待创建的目录路径字符串。
    :return: 成功创建或已存在的目录的 Path 对象。
    """
    # 强制将输入转换为 Path 对象
    path = Path(path)
    # 递归创建目录，并忽略目录已存在的情况
    path.mkdir(parents=True, exist_ok=True)
    return path

# def join(*paths: str | Path) -> Path:
#     """路径拼接工具函数。"""
#     result = Path(paths[0])
#     for p in paths[1:]:
#         result /= p
#     return result
# # 文件读取与写入
#
# def read_text(path: str | Path, encoding: str = "utf-8") -> str:
#     """读取文本文件内容。"""
#     return Path(path).read_text(encoding=encoding)
#
#
# def write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
#     """写入文本内容（自动创建父目录）。"""
#     p = Path(path)
#     p.parent.mkdir(parents=True, exist_ok=True)
#     p.write_text(content, encoding=encoding)
#
#
# # 文件遍历
# def list_files(dir_path: Union[str, Path], suffix: Optional[str] = None) -> List[Path]:
#     """
#     列出目录下所有文件（可按后缀过滤）。
#     """
#     d = Path(dir_path)
#     if not d.is_dir():
#         return []
#
#     files = [p for p in d.iterdir() if p.is_file()]
#     if suffix:
#         files = [p for p in files if p.suffix == suffix]
#
#     return files
# if __name__ == '__main__':
# print(__file__)
# print(__name__)
    # print(__path__)