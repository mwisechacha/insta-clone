from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    bio = models.TextField()
    pronouns = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    # link to another page 



