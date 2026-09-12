"""ask.py
提问的模型
"""
# 内置库
from pathlib import Path
# 第三方库
from pydantic import BaseModel


# 问题模型
class AskModel(BaseModel):
    question: str
    files: str | Path | list[str | Path] | None = None