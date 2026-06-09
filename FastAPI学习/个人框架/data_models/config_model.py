"""config_model.py
用户配置模型
"""
# 第三方库
from pydantic import BaseModel

class ConfigModel(BaseModel):
    """用户配置模型"""
    # 服务器模型
    server: ServerConfig
