

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # Specify the fields to be displayed
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'date_of_birth', 'profile_picture', 'address', 'is_vip')}),  # Add your custom fields here
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'date_of_birth', 'profile_picture', 'address', 'is_vip')}),  # Add custom fields for add form
    )

# Register your CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
