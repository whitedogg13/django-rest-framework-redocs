from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib import admin


class User(AbstractBaseUser):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    email = models.EmailField(unique=True, verbose_name='email address', max_length=255)
    full_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    file = models.FileField(upload_to='media/user_upload', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'full_name']


admin.site.register(User)
