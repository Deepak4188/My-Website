from django.urls import path
from . import views

urlpatterns = [
    path("", views.addItem, name="items")
]
