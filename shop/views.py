from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from django.urls import path

from . models import Category, Product
from . import views


def index(request):
    
    context = {}
    return render(request, 'shop/index.html')

def about(request):
    
    context ={}
    return render(request, 'shop/about.html')
    
def FAQ(request):
    
    context ={}
    return render(request, 'shop/FAQ.html')
