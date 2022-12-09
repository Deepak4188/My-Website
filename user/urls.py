from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("login", views.loginUser, name="login"),
    path("register", views.register, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('add', views.addItem, name="add"),
    path('addAddress', views.addAddress, name="address"),
    path('mycart', views.cart, name="mycart"),
    path('pay', views.payment, name="payment"),
    path('paymentStatus', views.paymentStatus, name="paymentStatus")
]
