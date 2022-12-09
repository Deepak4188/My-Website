from django.shortcuts import render, redirect
from shop.models import Product
from user.models import Persons

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    person = request.user
    products = Product.objects.all()
    n = len(products)
    params = {"no_of_slides":n, "range": range(n), "product":products, "user":person.username, "userId":person.userId}
    return render(request, "home.html", params)

def productDesc(request, id):
    person = request.user
    product = Product.objects.filter(productId=id)
    params = {"product":product, "user":person.username, "userId":person.userId}
    return render(request, "description.html", params)