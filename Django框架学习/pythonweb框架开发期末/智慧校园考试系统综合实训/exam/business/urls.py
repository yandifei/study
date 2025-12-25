# -*- coding: utf-8 -*-



from business import biz_render

from django.urls import path

urlpatterns = [
    path('', biz_render.home, name='index'),
    path('notify', biz_render.notify, name='notify'),
]