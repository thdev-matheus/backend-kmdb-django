from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUser(UserAdmin):
    readonly_fields = ("updated_at", "date_joined", "last_login")

    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("email", "first_name", "last_name", "birthdate", "bio")},
        ),
        ("Function Info", {"fields": ["is_critic"]}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
        ("Dates", {"fields": ("updated_at", "date_joined", "last_login")}),
    )


admin.site.register(User, CustomUser)
