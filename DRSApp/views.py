from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

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
    current_user = request.user
    total_docs_uploaded = models.Upload.objects.all().count()
    formatted_total_uploaded_docs = f"{total_docs_uploaded:,}"
    
    total_users = models.AuthModel.objects.all().count()
    formatted_total_users = f"{total_users:,}"
    
    total_pending_approvals = models.Upload.objects.filter(status='pending').count()
    formatted_total_pending_approvals = f"{total_pending_approvals}"
    context = {
        "total_docs_uploaded": formatted_total_uploaded_docs,
        "total_users": formatted_total_users,
        "total_pending_approvals": formatted_total_pending_approvals,
        "current_user": current_user
    }
    return render(request, 'dash/dashboard.html', context)

@login_required(login_url='/login')
def manage_users(request):
    all_users = models.AuthModel.objects.filter(role='user').order_by('-id')
    context = {
        "users": all_users
    }
    return render(request, 'dash/manage-users.html', context)

@login_required(login_url='/login/')
def user_details(request, id):
    try:
        user = models.AuthModel.objects.get(id=id)
    except:
        return JsonResponse({
            "message": f"Sorry we couldn't find a User with this ID - {id}",
            "success": False
        })
    
    context = {
        "user": user
    }
    return render(request, 'dash/userdetails.html', context)

@login_required(login_url='/login/')
def manage_documents(request):
    current_user = models.AuthModel.objects.filter(username=request.user).first()
    all_uploads = models.Upload.objects.all().order_by("-id")
    if request.method == 'POST':
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        file = request.FILES.get("file", "")
        
        max_size = 10 * 1024 * 1024  # 10MB
        
        if current_user:
            if file and file.name.lower().endswith(('.pdf', '.mp3', '.wav')) and file.size <= max_size:
                file_type = 'audio' if file.name.lower().endswith(('.mp3', '.wav')) else 'pdf'
                models.Upload.objects.create(
                    user=current_user, title=title, description=description, file=file, file_type=file_type
                )
                
                return JsonResponse({
                    "message": "Document uploaded successfully...",
                    "success": True
                })
            else:
                return JsonResponse({
                    "message":"Sorry your file size must be below 10MB!!",
                    "success": False
                })
        
        else:
            return JsonResponse({
                "message": "Sorry we couldn't detect any Active user!!",
                "success": False
            })

    context = {
        "uploads": all_uploads
    }
        
        
    return render(request, "dash/manage-docs.html", context)

@login_required(login_url='/login/')
def view_document(request, id):
    document = models.Upload.objects.filter(id=id).first()
    context = {
        "document": document
    }
    return render(request, "dash/view-documents.html", context)

@login_required(login_url='/login/')
@require_POST
def update_upload_status(request, id):
    doc = get_object_or_404(models.Upload, id=id)
    
    doc.status = "approved"
    doc.save()

    return JsonResponse({
        "message": f"Document {doc.title} approved successfully",
        "success": True,
        "id": doc.id,
        "status": doc.status,
    })