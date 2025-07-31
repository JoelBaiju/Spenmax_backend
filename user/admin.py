# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     # Customize the admin view if needed
#     pass

admin.site.register(CustomUser)

