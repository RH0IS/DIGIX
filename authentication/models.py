from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user= models.OneToOneField('auth.User',on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    registered = models.BooleanField(default=False)



