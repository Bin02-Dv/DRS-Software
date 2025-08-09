from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    return render(request, 'search.html')

def dash(request):
    return render(request, 'dash/dashboard.html')