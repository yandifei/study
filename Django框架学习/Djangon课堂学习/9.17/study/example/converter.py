from django.urls import register_converter


class MyConverter:
    regex = '1[3-9]\d{9}'# 匹配规则
    def to_python(self, value):
        return value
    def to_url(self, value):
        return value

# # 注册自定义的路由转换器
register_converter(converter=MyConverter, type_name='mobile')
