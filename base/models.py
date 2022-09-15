from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField as BaseCloudinaryField
# from django.utils import timesince


# Create your models here.

class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
            'public_id': model_instance.name,
            'unique_filename': False,
            'resource_type': 'image',
            'folder': "ezpizza/users/avatars/",
            'overwrite': True,       
            'invalidate': True,            
        }



class User(AbstractUser):
    name = models.CharField(max_length=64, null=True, unique=True)
    email = models.EmailField(unique=True)
    avatar = CloudinaryField('avatar', default='ezpizza/users/avatars/default_avatar.jpg')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    