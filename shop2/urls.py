from django.urls import path
from . import views

app_name = 'shop2'

urlpatterns = [

# Baking course view
    path('', views.product_list, name='product_list'),
    path('available-sessions/', views.available_course_sessions, name='available_course_sessions'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]




"""

    path('', views.product_list, name='product_list'),
    path('Products', views.product_list, name='product_list'),

    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    path('instructors', views.instructors, name='instructors'),
    path('registration', views.registration, name='registration'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart')
"""


