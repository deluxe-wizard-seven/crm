from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, AddRecordForm
from .models import Record

# Create your views here.

# Method/Function based view

# User Views

def user_login(request):
    """Logs in the user. This is also the default home page."""

    # When the user tries to log in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if user := authenticate(username=username, password=password):
            login(request, user)
            messages.success(request, "Successfully Logged In")
        else:
            messages.error(request, "Could not log you in. Please check the credentials")
        return redirect("home")

    # When user is authenticated then show the list of records
    elif request.user.is_authenticated:
        records = Record.objects.all()
        return render(request, "home.html", {"records": records})

    # When the user is not authenticated then don't show the list of records
    else:
        return render(request, "home.html", {})

def user_logout(request):
    """Logs out the user."""

    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("home")

def user_create(request):
    """Creates a new user and store their data in the database."""

    # When the user submits the registration form after filling up
    if request.method == "POST":
        fields = RegistrationForm.Meta.fields
        params = { field: request.POST.get(field) for field in fields }
        
        # Checking whether the username is already present in the database or not
        if User.objects.filter(username=params["username"]).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect("register")

        # Confirming the password
        elif params["password1"] != params["password2"]:
            messages.error(request, "Password Confirmation Failed.")
            return redirect("register")

        # Trying to create the user from the data provided from the user in the registration form and redirect to the login page
        else:
            user = RegistrationForm(request.POST)

            # If the form data is valid then save it and show success message
            if user.is_valid():
                user.save()
                messages.success(request, "User registered successfully.")
                return redirect("login")

            # When the form data is invalid then send the error messages to the HTML page which will prompt the user where they went wrong
            else:
                return render(request, "register.html", context={"form": user})

    # When the user is not submitting the form then we are sending the blank form to the user
    else:
        form = RegistrationForm()
        return render(request, "register.html", context={"form": form})

# Record Views

def record_create(request):
    """Used to create a record."""

    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record added successfully.")
            return redirect("home")
        else:
            return render(request, "add_record.html", { "form": form })
    else:
        form = AddRecordForm()
        return render(request, "add_record.html", { "form": form })

def record_retrieve(request, pk):
    """Used to retrive the record with the given primary key pk."""

    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        messages.success(request, f"Record(id={pk}) fetched successfully.")
        return render(request, "record.html", { "customer_record": record })
    else:
        messages.error(request, "You must be logged in, in order to retrieve the record details.")
        return redirect("home")

def record_update(request, pk):
    """Used to update the record with the given primary key pk."""

    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record(id={pk}) has been updated.")
            return redirect("home")
        else:
            messages.error(request, f"Record(id={pk}) was not updated.")
            return render(request, "update_record.html", { "form": form, "record_id": pk })
    else:
        messages.error(request, "You must be logged in, in order to update the record.")
        return redirect("home")

def record_delete(request, pk):
    """Used to delete the record with the given primary key pk."""

    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, f"Record(id={pk}) has been deleted successfully.")
        return redirect("home")
    else:
        messages.error(request, "You must be logged in, in order to delete the record.")
        return redirect("home")
