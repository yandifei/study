import subprocess
import os
import webbrowser
import time


def start_label_studio(port=8080):
    print(f"正在准备启动 Label Studio (端口: {port})...")

    # 构建启动命令
    # --port 指定端口, --user-data-dir 可以指定数据存储位置（可选）
    cmd = ["label-studio", "start", "--port", str(port)]

    try:
        # 启动子进程
        # stdout=None 表示直接将日志输出到当前的控制台
        process = subprocess.Popen(cmd)

        print("等待服务响应...")
        time.sleep(5)  # 等待几秒让服务完全启动

        # 自动打开浏览器
        webbrowser.open(f"http://localhost:{port}")

        print("Label Studio 已启动。关闭此 Python 程序将停止标注服务。")
        process.wait()

    except FileNotFoundError:
        print("错误：未找到 label-studio 命令。请确保已经运行了 'pip install label-studio'")
    except KeyboardInterrupt:
        print("\n正在停止标注服务...")
        process.terminate()


if __name__ == "__main__":
    start_label_studio(8080)

# 如何让标注员通过 IP 访问？
# 如果你想让同局域网的同事也能看到你的标注页面，只需修改命令中的 host 参数：
# 修改这一行
cmd = ["label-studio", "start", "--port", "8080", "--host", "0.0.0.0"]