# 第三方库
from pydantic import BaseModel

class Deepseek(BaseModel):
    """深度求索的配置类"""
    # 深度求索的名称
    display_name: str = "深度求索"
    # 登录的URL
    login_url: str = "https://chat.deepseek.com/sign_in"
    # 聊天的URL
    chat_url: str = "https://chat.deepseek.com/"
