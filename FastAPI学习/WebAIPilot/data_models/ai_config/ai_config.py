# 第三方库
from pydantic import BaseModel
# 内置库
from data_models.ai_config.deepseek import Deepseek
from data_models.ai_config.doubao import Doubao
from data_models.ai_config.gemini import Gemini


class AIConfig(BaseModel):
    """AI模型"""
    # 启动模型
    startup_type: str = "deepseek"
    # 深度求索
    deepseek: Deepseek
    # 豆包
    doubao: Doubao
    # 哈基米
    gemini: Gemini
