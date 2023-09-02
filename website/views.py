from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.

# Method/Function based view

# User Views

def user_login(request):
    """Logs in the user. This is also the default home page."""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if user := authenticate(username=username, password=password):
            login(request, user)
            messages.success(request, "Successfully Logged In")
        else:
            messages.error(request, "Could not log you in. Please check the credentials")
        return redirect("home")
    return render(request, "home.html", {})

def user_logout(request):
    """Logs out the user."""

    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("home")

def user_create(request):
    """Creates a new user and store their data in the database."""

    if request.method == "POST":
        fields = RegistrationForm.Meta.fields
        params = { field: request.POST.get(field) for field in fields }
        
        # Checking whether the username is already present in the database or not
        if User.objects.filter(username=params["username"]).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect("register")
        elif params["password1"] != params["password2"]:
            messages.error(request, "Password Confirmation Failed.")
            return redirect("register")
        else:
            user = RegistrationForm(request.POST)
            if user.is_valid():
                user.save()
                messages.success(request, "User registered successfully.")
                return redirect("login")
            else:
                return render(request, "register.html", context={"form": user})
    else:
        form = RegistrationForm()
        return render(request, "register.html", context={"form": form})

# Record Views

def record_create(request):
    pass

def record_retrieve(request):
    pass

def record_update(request):
    pass

def record_delete(request):
    pass
