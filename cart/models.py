from django.db import models
from shop.models import Product
from user.models import Persons

# Create your models here.
class CartItem(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    userId = models.ForeignKey(Persons, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userId)
    