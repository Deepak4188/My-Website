from django.shortcuts import render, redirect
from cart.models import CartItem
from shop.models import Product
from user.models import Persons

def addItem(request):
    userId = request.user
    if request.method == "POST":
        productId = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print(cart)
        
        if cart:
            quantity = cart.get(productId)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(productId)
                        CartItem.objects.filter(productId=Product(productId)).delete()
                    else:
                        cart[productId] = quantity-1
                        CartItem.objects.filter(productId=Product(productId)).update(quantity=quantity-1)
                else:
                    cart[productId] = quantity+1
                    CartItem.objects.filter(productId=Product(productId)).update(quantity=quantity+1)
            else:
                cart[productId] = 1
                item = CartItem(productId=Product(productId), userId=userId, quantity=cart[productId])
                item.save()
        else:
            cart = {}
            cart[productId] = 1
            item = CartItem(productId=Product(productId), userId=userId, quantity=cart[productId])
            item.save()
        request.session['cart'] = cart
    
    return redirect("home")

