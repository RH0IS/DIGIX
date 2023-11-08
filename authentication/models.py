from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user= models.OneToOneField('auth.User',on_delete=models.CASCADE)
    registered = models.BooleanField(default=False)