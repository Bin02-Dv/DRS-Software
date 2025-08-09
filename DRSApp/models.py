from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


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
