from django.shortcuts import render, redirect
from user.models import Persons
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

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
                return redirect("home")
        else:
            messages.success(request, "Password not matched!")
    return render(request, "register.html")
    


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            if Persons.objects.filter(email=email)[0].password == password:
                login(request, Persons.objects.filter(email=email)[0])
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