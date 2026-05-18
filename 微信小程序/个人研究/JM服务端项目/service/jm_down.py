"""jm_down.py
禁漫天堂本子下载
"""
# 内置库
import os
import shutil

# 第三方库
from jmcomic import download_album, jm_exception, create_option_by_file

def download_jmcomic(album_id: str) -> tuple[str, bool]:
    """
    通过禁漫天堂 ID 下载本子（PDF 或图片文件夹）
    :param album_id: 本子 ID，例如 "422866"
    :return: 下载结果信息（成功/失败原因）
    """
    if not album_id or not isinstance(album_id, str):
        return "错误：请提供有效的字符串类型 album_id", False

    try:
        # 清理残留的资源(把整个缓存目录删除)和目录还原(目录创建回去)
        shutil.rmtree("./outputs/发送缓存")
        os.mkdir("./outputs/发送缓存")
        shutil.rmtree("./outputs/下载缓存")
        os.mkdir("./outputs/下载缓存")
    except FileNotFoundError:
        return "目录不存在，无需删除", False
    except (PermissionError, FileExistsError):
        # 满载第二次请求是PermissionError(shutil.rmtree)，带三次是FileExistsError(os.mkdir)
        return "请等待上一份的jm发送完再使用该指令(我不是服务器，垃圾CUP没法满足同时下载多个文件)，如您不能见谅请把您的CPU借我用用！", False

    try:
        # 读取配置（请确保路径下的 option.yml 存在且正确）
        option = create_option_by_file("./user_data/option.yml")
        download_album(album_id, option)
        return f"本子 {album_id} 下载成功", True
    except jm_exception.PartialDownloadFailedException as e:
        return f"部分下载失败：{str(e).split(': [', 1)[0]}", True
    except jm_exception.MissingAlbumPhotoException as e:
        return f"本子不存在：{str(e)}", False
    except jm_exception.JmcomicException as e:
        return f"下载异常：{str(e)}", False

if __name__ == '__main__':
    result = download_jm("422866")
    print(result)