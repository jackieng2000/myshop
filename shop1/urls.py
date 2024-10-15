from django.urls import path
from . import views


app_name = 'shop1'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('Products', views.product_list, name='product_list'),
    path('ordering/<int:id>/<slug:slug>', views.ordering, name='ordering'),
    path('ordering', views.ordering, name='ordering'),
    path('<int:id>', views.category_list, name='category_list'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]