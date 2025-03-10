from django.shortcuts import render

def home(request):
    return render(request, "home.html")  # This will look for a template named home.html
