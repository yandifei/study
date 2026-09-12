import os
import zipfile
import shutil
from label_studio_sdk import Client


def export_and_setup_yolo(api_key, project_id, output_dir):
    # 1. 初始化客户端
    ls = Client(url='http://localhost:8080', api_key=api_key)

    # 强制检查 Token 是否可用
    try:
        # 这里会直接触发一次 API 请求来验证身份
        user = ls.make_request('GET', '/api/users/me')
        print(f"✅ 身份验证成功！欢迎: {user.json().get('email')}")
    except Exception as e:
        print(f"❌ 身份验证失败，请确认 Token 是否最新: {e}")
        return

    # 2. 导出数据集
    print(f"正在从项目 {project_id} 导出 YOLO 格式数据...")
    project = ls.get_project(int(project_id))

    # 导出并获取二进制流
    export_data = project.export_tasks(export_type="YOLO", download_resources=True)

    # 保存压缩包
    zip_path = os.path.join(output_dir, 'export.zip')
    os.makedirs(output_dir, exist_ok=True)
    with open(zip_path, 'wb') as f:
        f.write(export_data)
    print(f"✅ 压缩包已下载: {zip_path}")

    # 3. 自动解压
    raw_extract_path = os.path.join(output_dir, 'raw_data')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(raw_extract_path)
    print(f"✅ 数据已解压至: {raw_extract_path}")

    # 4. 后续建议
    print("\n下一步提示：")
    print(f"1. 进入 {raw_extract_path} 查看图片和 labels 文件夹。")
    print(f"2. 使用我之前给你的 'split_data.py' 脚本对该文件夹进行训练/验证集划分。")


# --- 配置区 ---
# 请使用你刚刚重新生成的 Token
MY_TOKEN = ""
PROJECT_ID = "2"
SAVE_PATH = "./"

if __name__ == "__main__":
    export_and_setup_yolo(MY_TOKEN, PROJECT_ID, SAVE_PATH)