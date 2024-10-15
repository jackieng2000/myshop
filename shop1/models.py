from django.db import models
from django.urls import reverse
from datetime import datetime
from shop.models import Category, Product #ForeignKey
from django.utils import timezone

class ProductDetail(models.Model): # Table Name: ProductDetail
    CAKE_SIZES = [
        ('12cm', '12cm'),
        ('18cm', '18cm'),
        ('22cm', '22cm'),
        ('28cm', '28cm'),
    ]

    CAKE_WEIGHT = [
        ('400g', '400g'),
        ('850g', '850g'),
        ('1.2kg', '1.2kg'),
        ('1.8kg', '1.8kg'),
    ]

    CAKE_DESC = [
        ('For 3 - 4 persons', 'For 3 - 4 persons'),
        ('For 8 - 10 persons', 'For 8 - 10 persons'),
        ('For 10 - 12 persons', 'For 10 - 12 persons'),
        ('For 18 - 20 persons', 'For 18 - 20 persons'),
    ]

    id = models.AutoField(primary_key=True) # key

    allergen = models.TextField(blank=True) # text field / blank = true

    First_size = models.CharField(max_length=50, default="12cm", choices=CAKE_SIZES) # choices="12cm" 
    First_weight = models.CharField(max_length=50, default="400g", choices=CAKE_WEIGHT) # choices="400g"
    First_desc = models.CharField(max_length=50, default="For 3 - 4 persons", choices=CAKE_DESC) # choices="For 3 - 4 persons"
    First_price = models.IntegerField()

    Second_size = models.CharField(max_length=50, default="18cm", choices=CAKE_SIZES) # choices="18cm" 
    Second_weight = models.CharField(max_length=50, default="850g", choices=CAKE_WEIGHT) # choices="850g"
    Second_desc = models.CharField(max_length=50, default="For 8 - 10 persons", choices=CAKE_DESC) # choices="For 8 - 10 persons"
    Second_price = models.IntegerField()

    Third_size = models.CharField(max_length=50, default="22cm", choices=CAKE_SIZES) # choices="22cm" 
    Third_weight = models.CharField(max_length=50, default="1.2kg", choices=CAKE_WEIGHT) # choices="1.2kg"
    Third_desc = models.CharField(max_length=50, default="For 10 - 12 persons", choices=CAKE_DESC) # choices="For 10 - 12 persons"
    Third_price = models.IntegerField()

    Fourth_size = models.CharField(max_length=50, default="28cm", choices=CAKE_SIZES) # choices="22cm" 
    Fourth_weight = models.CharField(max_length=50, default="1.8kg", choices=CAKE_WEIGHT) # choices="1.8kg"
    Fourth_desc = models.CharField(max_length=50, default="For 18 - 20 persons", choices=CAKE_DESC) # choices="For 18 - 20 persons"
    Fourth_price = models.IntegerField()

    product = models.ForeignKey(Product,
                                 related_name='product_detail',
                                 on_delete=models.PROTECT)
    
    name = models.CharField(max_length=50, default="no name", blank=True, null=True)  
    
    def __str__(self):
        return self.name

class Cakes(models.Model):
    CAKE_SIZES = [
        ('12cm', '12cm'),
        ('18cm', '18cm'),
        ('22cm', '22cm'),
        ('28cm', '28cm'),
    ]

    CAKE_WEIGHT = [
        ('400g', '400g'),
        ('850g', '850g'),
        ('1.2kg', '1.2kg'),
        ('1.8kg', '1.8kg'),
    ]

    CAKE_DESC = [
        ('For 3 - 4 persons', 'For 3 - 4 persons'),
        ('For 8 - 10 persons', 'For 8 - 10 persons'),
        ('For 10 - 12 persons', 'For 10 - 12 persons'),
        ('For 18 - 20 persons', 'For 18 - 20 persons'),
    ]
    
    id = models.AutoField(primary_key=True) # key
    Cake_Sizes = models.CharField(max_length=50, choices=CAKE_SIZES)
    Cake_Weight = models.CharField(max_length=50, choices=CAKE_WEIGHT)
    Cake_Desc = models.CharField(max_length=50, choices=CAKE_DESC)

#    def __str__(self):
#        return self.name 
