# 第三方库
from pydantic import BaseModel

class Gemini(BaseModel):
    """Gemini的配置类"""
    # Gemini的名称
    display_name: str = "gemini"
    # 登录的URL
    login_url: str = "https://accounts.google.com/"
    # 聊天的URL
    chat_url: str = "https://gemini.google.com/app"
