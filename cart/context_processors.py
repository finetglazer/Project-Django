# cart/context_processors.py
from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.cart_items.count()
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0
    return {'cart_count': count}
