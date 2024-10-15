from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','shop_id','image']
    list_filter = ['shop_id']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10  # Limit the number of rows per page
    list_editable = ['image']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'name', 'slug','shop_id','price', 'image',
                    'available', 'created', 'updated']
    list_filter = ['available', 'shop_id','created', 'updated']
    list_editable = ['price', 'image', 'available']
    list_per_page = 10  # Limit the number of rows per page
    prepopulated_fields = {'slug': ('name',)}
