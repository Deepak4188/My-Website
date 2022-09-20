from django.urls import path
from . import views

urlpatterns = [
    path("home", views.index, name="home"),
    path("product/<int:id>", views.productDesc, name="product Description")
]
