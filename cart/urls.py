# cart/urls.py
from django.urls import path
from .views import cart_view, add_to_cart, cart_remove

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:customerId>/', cart_remove, name='cart_remove'),
    # You can add more paths, e.g. for removing items, checkout, etc.
]
