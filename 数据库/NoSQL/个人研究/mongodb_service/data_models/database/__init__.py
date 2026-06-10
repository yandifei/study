"""
data_models.database 包

pydantic BaseModel 数据模型，不依赖 ODM。
"""
from data_models.database.user import User

__all__ = [
    "User",
]
