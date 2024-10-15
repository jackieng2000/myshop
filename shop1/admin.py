from django.contrib import admin

# Register your models here.
from .models import Cakes, ProductDetail

class CakesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Cake_Sizes', 'Cake_Weight', 'Cake_Desc')
    list_display_links = ('id', 'Cake_Desc')
    search_fields = ('id',)
    list_per_page = 10
admin.site.register(Cakes, CakesAdmin)

class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'allergen', 'First_size', 'First_weight', 'First_desc', 'First_price', 'Second_size', 'Second_weight', 'Second_desc', 'Second_price', 'Third_size', 'Third_weight', 'Third_desc', 'Third_price', 'Fourth_size', 'Fourth_weight', 'Fourth_desc', 'Fourth_price', 'product')
    list_display_links = ('id', )
    list_filter = ['product']
    search_fields = ('id','product')
    list_per_page = 10
admin.site.register(ProductDetail, ProductDetailAdmin)
