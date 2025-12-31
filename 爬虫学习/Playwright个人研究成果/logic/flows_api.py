"""flows_api.py
统一接口
"""
from utils import ConfigManager
from utils.playwright_factory.playwright_factory import PlaywrightFactory


class FlowsAPI:
    """统一接口
    """
    def __init__(self, config_manager: ConfigManager, playwright_factory: PlaywrightFactory):
        self.cm: ConfigManager = config_manager
