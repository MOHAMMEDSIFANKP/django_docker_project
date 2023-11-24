from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    qrcode = models.ImageField(upload_to='qrcodes', null=True, blank=True)

    def __str__(self):
        return self.user.username