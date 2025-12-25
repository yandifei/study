# -*- coding: utf-8 -*-



from account import login_render, login_views, email_notify
from django.urls import path
# 登录url
urlpatterns = [
    path('login_redirect', login_views.login_redirect, name='login_redirect'),
    path('signup_redirect', login_render.signup_redirect, name='signup_redirect'),
    path('email_notify', login_render.email_notify, name='email_notify'),
    path('email_notify_new', email_notify.email_notify_new, name='email_notify_new'),
    path('reset_notify', login_render.reset_notify, name='reset_notify'),
]
