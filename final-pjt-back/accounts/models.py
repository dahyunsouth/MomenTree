from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    wealth = models.IntegerField(default=0)
    monthly_deposit = models.IntegerField(default=0)
    desire_period = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default.jpg')
    
    class Meta:
        db_table = 'user' 