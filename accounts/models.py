from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

#from django.contrib.auth import get_user_model
#User = get_user_model()

class CustomUser(AbstractUser):
    # Other fields for your custom user can go here

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_vip = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group,
        related_name='customuser_set',  # Change this to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change this to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.'
    )

#    pass



"""

Standard Fields in the User Model
username:   A unique identifier for the user. 
first_name:
last_name:
email:
password:
last_login:
is_active:
is_staff:
is_superuser:
date_joined:

Additional Fields

phone_number: For storing the user's phone number.
profile_picture: For storing a URL or file path to the user's profile image.
date_of_birth: To store the user's date of birth.
address: To store the user's address information.    
    # Add more fields as needed
"""