import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # 指向你的 settings 文件
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    # 默认启动 127.0.0.1:8000
    args = [sys.argv[0], "runserver", "127.0.0.1:8000", "--noreload"]
    execute_from_command_line(args)