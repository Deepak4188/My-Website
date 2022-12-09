from django.contrib.auth.models import AbstractUser
from django.db import models
from shop.models import Product

# Create your models here.

class Persons(AbstractUser):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "password")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.userId)


class Address(models.Model):
    addressId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(Persons, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=15)
    pinCode = models.CharField(max_length=10)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    houseNo = models.CharField(max_length=255)
    colony = models.CharField(max_length=255)
    addressType = models.CharField(max_length=15)

    def __str__(self):
        return str(self.addressId)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    orderId = models.CharField(max_length=255)
    razorpayPaymentId = models.CharField(max_length=255, blank=True)
    paid = models.BooleanField(default=False)
    userId = models.ForeignKey(Persons, on_delete=models.CASCADE)
    addressId = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    Amount = models.IntegerField(default=100)

    def __str__(self):
        return str(self.orderId)