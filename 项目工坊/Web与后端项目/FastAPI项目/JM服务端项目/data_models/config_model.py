"""config_model.py
用户配置模型
"""
# 第三方库
from pydantic import BaseModel
# 自己的模块
from data_models.server_config import ServerConfig


class ConfigModel(BaseModel):
    """用户配置模型"""
    # 服务器模型
    server: ServerConfig

