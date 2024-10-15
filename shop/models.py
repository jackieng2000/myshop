from django.db import models
from django.urls import reverse


class Category(models.Model):

    CHOICES = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
    ]
    id = models.AutoField(primary_key=True) # #key

    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True) # also unique key
    shop_id = models.IntegerField(default=1, choices=CHOICES)
    
    image = models.ImageField(upload_to='catagories',
                              blank=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_shop1_url(self):
        return reverse('shop1:product_list_by_category',
                       args=[self.slug])
    
    def get_absolute_shop2_url(self):
        return reverse('shop2:product_list_by_category',
                       args=[self.slug])
    
    def get_absolute_shop3_url(self):
        return reverse('shop3:product_list_by_category',
                       args=[self.slug])
    
    def get_absolute_shop4_url(self):
        return reverse('shop4:product_list_by_category',
                       args=[self.slug])



class Product(models.Model):
    CHOICES = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
    ]
    id = models.AutoField(primary_key=True) # key
    shop_id = models.IntegerField(default=1, choices=CHOICES)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.PROTECT)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_shop1_url(self):
        return reverse('shop1:product_detail',
                       args=[self.id, self.slug])
    
    def get_ordering_shop1_url(self):
        return reverse('shop1:ordering',
                       args=[self.id, self.slug])
                      
    def get_absolute_shop2_url(self):
        return reverse('shop2:product_detail',
                       args=[self.id, self.slug])
    
    def get_absolute_shop3_url(self):
        return reverse('shop3:product_detail',
                       args=[self.id, self.slug])
    
    
    def get_absolute_shop4_url(self):
        return reverse('shop4:product_detail',
                       args=[self.id, self.slug])
    
    
