from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def popup(request):
    return render(request, 'popup.html')

def index(request):
    return render(request, "index.html")

def logout(request):
    auth.logout(request)
    return redirect("/login/")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return JsonResponse({
                "message": "Login completed successfully.. Wecome to Fatwas Repository.",
                "success": True
            })
        else:
            return JsonResponse({
                "message": "Sorry your username or password is invalid!! Try again.",
                "success": False
            })
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")
        institution = request.POST.get("institution", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        confirm_password= request.POST.get("confirm_password", "")
        
        if models.AuthModel.objects.filter(username=username).exists():
            return JsonResponse({
                "message": f"Sorry this username '{username}' already exists!!",
                "success": False
            })
            
        elif models.AuthModel.objects.filter(email=email).exists():
            return JsonResponse({
                "message": f"Sorry this email '{email}' already exists!!",
                "success": False
            })
        
        elif confirm_password != password:
            return JsonResponse({
                "message": "Sorry your password and confirm password missed match!!",
                "success": False
            })
        
        else:
            models.AuthModel.objects.create_user(
                full_name=full_name, email=email, username=username, password=password, institution=institution, phone_number=phone_number
            )
            return JsonResponse({
                "message": "Sign Up completed successfully..",
                "success": True
            })
    return render(request, 'signup.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    return render(request, 'search.html')

@login_required(login_url='/login/')
def dash(request):
    return render(request, 'dash/dashboard.html')

@login_required(login_url='/login')
def manage_users(request):
    all_users = models.AuthModel.objects.filter(role='user').order_by('-id')
    context = {
        "users": all_users
    }
    return render(request, 'dash/manage-users.html', context)