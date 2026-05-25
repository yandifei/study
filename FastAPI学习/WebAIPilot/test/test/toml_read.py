# 仅适用于 Python 3.11 及以上版本
import json
import tomllib

from utils import get_root

config_file_path = get_root() / "user_data" /  "user_settings.toml"


# 'rb' 模式表示以二进制方式读取，这是 tomllib 的要求
with open(config_file_path, 'rb') as f:
    config_data = tomllib.load(f)
# print(config_data)
print(json.dumps(config_data))
