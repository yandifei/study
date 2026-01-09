"""server_model.py
服务器的模型
"""
# 内置库
from pathlib import Path
# 第三方库
from pydantic import BaseModel

# 问题模型
class ServerModel(BaseModel):
    protocol: str = "http"
    host: str = "127.0.0.1"
    port: int = 8000