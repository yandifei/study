"""__init__.py"""
# 只暴露公共 API
from utils.path_utils import get_root, is_path_exist, get_parent_path, mkdir
from dotenv import load_dotenv
__author__ = 'yandifei'

# 加载环境变量,不会覆盖系统中已存在的同名环境变量
load_dotenv(f"{get_root()}/config/.env")