from django.shortcuts import render, redirect
from user.models import Persons
from shop.models import Product
from cart.models import CartItem
from django.contrib import messages
from django.contrib.auth import logout, login

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if password == re_password:
            if Persons.objects.filter(email=email).exists():
                messages.info(request, "You are already registered!")
                return redirect("login")
            else:
                entry = Persons(username=name, email=email, password=password)
                entry.save()
                messages.success(request, "You have been registered!")
                return redirect("login")
        else:
            messages.success(request, "Password not matched!")
    return render(request, "register.html")
    


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = Persons.objects.filter(email=email)
        try:
            if Persons.objects.filter(email=email)[0].password == password:
                login(request, Persons.objects.filter(email=email)[0])
                request.session['userId'] = user[0].userId
                return redirect("shop/home")
            else:
                messages.error(request, "Record not found!")
                return render(request, "login.html")
        except:
            messages.warning(request, "You have not registered!")   
            return redirect("register")
    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out!")
    return render(request, "login.html")

def cart(request):
    user = request.user
    products = CartItem.objects.filter(userId=user)
    productIds = {}
    amount = 0.0
    for i in range(len(products)):
        productIds[products[i].productId] = products[i].quantity
        amount += (products[i].productId).productPrice*products[i].quantity
    params = {"product":productIds, "user":user.username, "total":amount}
    return render(request, "cart.html", params)

def addItem(request):
    userId = request.user
    if request.method == "POST":
        productId = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = CartItem.objects.filter(userId=userId)
        
        if cart:
            product = CartItem.objects.filter(productId=productId, userId=userId)
            
            if len(product) > 0:
                quantity = product[0].quantity
            else:
                quantity = 0
            if quantity:
                if remove:
                    if quantity == 1:
                        CartItem.objects.filter(productId=Product(productId)).delete()
                    else:
                        quantity = quantity-1
                        CartItem.objects.filter(productId=Product(productId)).update(quantity=quantity)
                else:
                    quantity = quantity+1
                    CartItem.objects.filter(productId=Product(productId)).update(quantity=quantity)
            else:
                quantity = 1
                item = CartItem(productId=Product(productId), userId=userId, quantity=quantity)
                item.save()
        else:
            quantity = 1
            item = CartItem(productId=Product(productId), userId=userId, quantity=quantity)
            item.save()
    link = "/shop/home#"+str(Product(productId))
    return redirect(link)