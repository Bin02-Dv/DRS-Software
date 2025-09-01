from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def user_upload_path(instance, filename):
    return f"{instance.user.full_name}/files/{filename}"


class AuthModel(AbstractUser):
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=200, blank=True, unique=True)
    role = models.CharField(default='user')
    institution = models.CharField(max_length=250, blank=True)
    password = models.CharField(max_length=250, blank=True)
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = []


class Upload(models.Model):
    user = models.ForeignKey(AuthModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True, max_length=200)
    file = models.FileField(upload_to=user_upload_path)
    upload_date =  models.DateField(auto_now_add=True)
    file_type = models.CharField(max_length=20, blank=True, default="audio")
    status = models.CharField(max_length=30, default="pending")
    topic = models.CharField(max_length=50, blank=True, null=True, default='test')
