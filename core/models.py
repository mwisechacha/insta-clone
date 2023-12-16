from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField()
    pronouns = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    # link to another page


