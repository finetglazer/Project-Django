from django.urls import path
from . import views

urlpatterns = [
    path('item/search', views.search, name='search'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('db-health/', views.db_health_check, name='db_health_check'),
]