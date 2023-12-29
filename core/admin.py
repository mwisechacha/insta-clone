from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from .relationship import Relationship
from .models import User

# Register your models here.    
class UserProfileAdmin(admin.StackedInline):
     model = models.Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
     inlines = [UserProfileAdmin]
     add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )
     

admin.site.register(models.Relationship)