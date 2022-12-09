from django.contrib import admin
from user.models import Persons, Address, Order
# Register your models here.

admin.site.register(Persons)
admin.site.register(Address)
admin.site.register(Order)