from django.urls import path
from . import views

app_name = 'shop3'

urlpatterns = [
    path('', views.baking_studio, name='baking_studio'),
    path('Baking_studio', views.baking_studio, name='baking_studio'),
    path('Booking', views.booking, name='booking'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('Booking_information', views.product_list, name='product_list'),
    path('Products/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

