from django.db import models
from django.conf import settings  # Add this import for AUTH_USER_MODEL
from decimal import Decimal

# Make sure Item model is defined BEFORE Review model
class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='items/', blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name

    def get_price_as_decimal(self):
        # If self.price is a Decimal128
        if hasattr(self.price, 'to_decimal'):
            return Decimal(self.price.to_decimal())
        return self.price


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    sentiment_score = models.FloatField(default=0.0)  # Will store our sentiment analysis result
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.item.name}"