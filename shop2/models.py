from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from shop.models import Product
from shop3.models import Studio
from django.utils import timezone

def validate_time(value):
    # Define allowed times
    allowed_times = [(9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0)]  # (hour, minute) tuples
    
    # Check if the time is in allowed times
    if (value.hour, value.minute) not in allowed_times:
        raise ValidationError(f"Start time must be one of the following: {allowed_times}.")


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True) # #key
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True,default="")
    description = models.TextField()
    image = models.ImageField(upload_to='menuitem',
                              blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name  


class Instructor(models.Model):
    id = models.AutoField(primary_key=True) # key
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, db_index=True, default="")
    description = models.TextField()
    image = models.ImageField(upload_to='instructor',
                              blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name  


class CourseSession(models.Model): 
    id = models.AutoField(primary_key=True) # key
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True, default="")
    product_id = models.ForeignKey(Product,
                                 related_name='products',
                                 on_delete=models.PROTECT)
    contents = models.TextField()
    menu_name= models.ForeignKey(MenuItem,
                                 related_name='menuitems',
                                 on_delete=models.PROTECT)
    instructor = models.ForeignKey(Instructor, 
                                    related_name='instructors',
                                    on_delete=models.PROTECT)
    start_date_time = models.DateTimeField(validators=[validate_time])
    end_date_time = models.DateTimeField(validators=[validate_time])
    studio_name = models.ForeignKey(Studio,
                                 related_name='studios',
                                 on_delete=models.PROTECT)
    location = models.CharField(max_length=100)
    quota = models.IntegerField(default=0)
    filled_place = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100)


    def __str__(self):
        return self.name  
    
    def get_absolute_shop2_url(self):
        return reverse('shop2:product_detail',
                       args=[self.id, self.slug])


