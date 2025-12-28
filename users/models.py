from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    full_name = models.CharField(verbose_name='full_name', max_length=255, blank=True)
    avatar = models.URLField(verbose_name='avatar', blank=True, null=True)
