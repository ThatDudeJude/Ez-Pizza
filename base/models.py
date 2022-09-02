from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils import timesince


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=64, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, default='default_avatar.svg')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    


