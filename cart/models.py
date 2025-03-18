# cart/models.py
from django.db import models
from django.conf import settings
from book.models import Item  # Import your Item model from the book app


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        total = sum(cart_item.total_price() for cart_item in self.cart_items.all())
        return total

    def __str__(self):
        return f"Cart for {self.user.username}" if self.user else "Anonymous Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    from decimal import Decimal

    def total_price(self):
        price = self.item.price
        # If price is a Decimal128 instance, convert it to a Python Decimal
        if hasattr(price, 'to_decimal'):
            price = price.to_decimal()
        return price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
