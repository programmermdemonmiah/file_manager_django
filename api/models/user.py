from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.timezone import now
from file_manager import PROFILE_IMAGE_UPLOAD_DIR

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=150, unique=True, null=False, db_index=True)
    email = models.EmailField(unique=True, null=False, db_index=True)
    password = models.CharField(max_length=255) 
    image = models.ImageField(upload_to=PROFILE_IMAGE_UPLOAD_DIR, null=True, blank=True)
    fcm_token = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users' 

    def __str__(self):
        return self.username
