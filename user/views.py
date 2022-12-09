from django.shortcuts import render, redirect
from user.models import Persons, Address, Order
from shop.models import Product
from cart.models import CartItem
from django.contrib import messages
from django.contrib.auth import logout, login
import razorpay


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
    if request.user.is_anonymous:
        return redirect("/login")
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


def addAddress(request):
    userId = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        number = request.POST.get('phone')
        pinCode = request.POST.get('pin')
        state = request.POST.get('state')
        city = request.POST.get('city')
        house = request.POST.get('house')
        area = request.POST.get('area')
        addressType = request.POST.get('type') 

        address = Address(userId=userId, fullName=name, phoneNumber=number, pinCode=pinCode, state=state, city=city, houseNo=house, colony=area, addressType=addressType)
        address.save()
        return redirect("/pay")
        

def payment(request):
        userId = request.user
        products = CartItem.objects.filter(userId=userId)
        if not products:
            return redirect("/mycart")

        client = razorpay.Client(auth=('rzp_test_4ui8SgVe9QiQQu', 'oMPpGMxWWzn8hWdhaif1kISJ'))

        amount = 0.0
        for i in range(len(products)):
            amount += (products[i].productId).productPrice*products[i].quantity

        amount *= 100
        responsePayment = client.order.create(dict(amount=amount, currency='INR'))
        orderId = responsePayment['id']
        orderStatus = responsePayment['status']
        orderId = str(orderId)
        address = Address.objects.filter(userId=userId)
        noOfAddress = len(address)
        if orderStatus == 'created':
            responsePayment['name'] = userId.username
            for i in range(len(products)):
                order = Order(orderId=orderId, userId=userId, productId=(products[i].productId), quantity=int(products[i].quantity), Amount=amount/100)
                order.save()
            return render(request, "payment.html", {'payment':responsePayment, "address":address, "noOfAddress":noOfAddress, 'user':userId.username, 'email':userId.email})
        return redirect("/mycart")


def paymentStatus(request):
    userId = request.user
    response = request.POST
    addressId = request.POST.get("addressId")
    client = razorpay.Client(auth=('rzp_test_4ui8SgVe9QiQQu', 'oMPpGMxWWzn8hWdhaif1kISJ'))
    try:
        status = client.utility.verify_payment_signature({
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
        })
        Order.objects.filter(orderId = response['razorpay_order_id']).update(razorpayPaymentId=response['razorpay_payment_id'], paid=True, addressId=addressId)
        CartItem.objects.filter(userId=userId).delete()
        return render(request, "paymentStatus.html", {'status':True, 'user':userId.username})
    except:
        return render(request, "paymentStatus.html", {'status':False})