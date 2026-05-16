“多模态+安防+流水线”
Multi-Modal Security Pipeline
MMSP

这还是第一次如此紧急的开发一个能用的系统呢（一晚上呢，如果是AI全力我1小时干爆，可惜我得要了解项目呢）
且这个系统还得是我自己了解的，不然我真想一个CLI下去直接干出来
抄你妈的队长，我一个人负责所有东西，你就安详考研复习是吧

奇迹吗？只有有人替你负重前行了
“所谓奇迹，并不是等待它降临。而是大家一起努力，共同达成的终点。那就是奇迹！”
名为勇气是最强的魔法


[config_manager.py](utils/config_manager.py)
数据模型，企业级开发配置
```python
# # 初始化配置数据(字典) 高级的时候采用数据模型
# self.config_data: dict | ConfigModel = {}
```

修复[config_manager.py](utils/config_manager.py)
```python
        if (json := self.load_toml(get_root() / "config" / "settings.toml")) is not False:
```
这个代码是修复好的，如果直接if 对面返回的空地址也会被认为是False，以后还是注意数据类型指定吧