from django.db import models

class Product(models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    productPrice = models.FloatField()
    productImage = models.CharField(max_length=400)
    productDescription = models.CharField(max_length=500)


    def __str__(self):
        return str(self.productId)
    