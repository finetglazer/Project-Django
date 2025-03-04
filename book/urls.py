from django.urls import path
from . import views

urlpatterns = [
    path('item/search', views.search, name='search'),
]
