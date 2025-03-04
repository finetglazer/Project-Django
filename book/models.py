from django.db import models
from decimal import Decimal


class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='items/', blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    # Add more fields as needed

    def __str__(self):
        return self.name

    def get_price_as_decimal(self):
        # If self.price is a Decimal128
        if hasattr(self.price, 'to_decimal'):
            return Decimal(self.price.to_decimal())
        return self.price
