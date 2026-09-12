from django.urls import register_converter
class MyConverter:
    # 匹配规则
    regex = '1[3-9]\d{9}'
    def to_python(self, value):
        return value
    def to_url(self, value):
        return value
# 注册自定义的路由转换器
register_converter(converter=MyConverter, type_name='mobile')



