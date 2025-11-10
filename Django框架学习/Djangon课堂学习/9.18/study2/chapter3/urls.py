#chapter3\chapter3\urls.py
from django.urls import path,include
from django.urls import re_path
from . import views
from testinclude import views as subViews
sub=[path('sub2/',subViews.useinclude),]
urlpatterns = [
    re_path(r'^[A-Za-z]+$',views.CharInUrl),  #匹配大小写字母组成的字符串
    re_path(r'^\d{2,}$',views.NumberInUrl),   #匹配至少两位数字组成的数字字符串
    path('root/', include('testinclude.urls')),  #包含应用testinclude的URL配置
    path('root2/', include(sub)),  #包含应用testinclude的URL配置
    path('test/<urlData>/', views.getData),
    path('test/<Data1>/<Data2>/', views.getData2),
    path('data1/<str:data>', views.getData1),
    path('data2/<int:data>', views.getData2),
    path('data3/<slug:data>', views.getData3),
    path('data4/<uuid:data>', views.getData4),
    path('data5/<path:data>', views.getData5), 
    re_path(r'^reex/(?P<data>[a-z0-9]+)$', views.getReData),
    path('extra/<data>', views.getExtraData,{"ex":"123"}),
    path('default/', views.useDefault),          #参数data使用默认值
    path('default/<data>/', views.useDefault),    #参数data使用URL数据
    path('rev/abc', views.getUrlNoPara,name="urlNoPara"), 
    path('rev2/<data>', views.getUrlArgs,name="UrlArgs"), 
    path('rev3/<data>', views.getUrlKwargs,name="UrlKwargs"),
    path('rev4/test', views.getViewUrl), 
    path('uset/<path:data>',views.reverseInTemplates,name='urlTemplate'),

    path('usename1/',include('useAppNamespace.urls')),     #第一个useAppNamespace应用实例
    path('usename2/',include('useAppNamespace.urls')),     #第二个useAppNamespace应用实例

    path('usename3/',include('useInstanceNamespace.urls',namespace="nameIndex")),     
    path('usename4/',include('useInstanceNamespace.urls',namespace="nameIndex2")),

]