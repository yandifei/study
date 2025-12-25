from django.urls import path

app_name = 'indexes'
from . import views

urlpatterns = [
    # 商品列表页
    path('list/<int:category_id>/<int:page_num>/', views.ListView.as_view(), name='list'),
    path('hot/<int:category_id>/', views.HostGoodsView.as_view()),
    path('detail/<int:sku_id>/', views.DetailView.as_view(), name='detail'),
]
