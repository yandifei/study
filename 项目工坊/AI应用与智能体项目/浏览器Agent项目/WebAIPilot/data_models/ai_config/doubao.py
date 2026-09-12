# 第三方库
from pydantic import BaseModel

class Doubao(BaseModel):
    """豆包的配置类"""
    # 豆包的名称
    display_name: str = "豆包"
    # 登录的URL
    login_url: str = "https://www.doubao.com/chat/"
    # 聊天的URL
    chat_url: str = "https://www.doubao.com/chat/"


# [AI.doubao]
# display_name = "豆包"
# login_url = "https://www.doubao.com/chat/"
# chat_url = "https://www.doubao.com/chat/"
#
# [AI.deepseek]
# display_name = "深度求索"
# login_url = "https://chat.deepseek.com/sign_in"
# chat_url = "https://chat.deepseek.com/"
#
# [AI.gemini]
# display_name = "gemini"
# login_url = "https://accounts.google.com/"
# chat_url = "https://gemini.google.com/app"
