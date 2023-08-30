from django.shortcuts import render

# Create your views here.

# Method/Function based view
def home(request):
    return render(request, "home.html", {})
