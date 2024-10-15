import calendar
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddProductForm
from shop.models import Category, Product
from shop1.models import ProductDetail
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from datetime import datetime, timedelta
from django.utils import timezone
from cart.cart import Cart
from cart.forms import CartAddProductForm
from decimal import Decimal
from django.conf import settings
from django.contrib.sessions.models import Session
import json
from decimal import Decimal
import uuid

def product_list(request, slug=None):

    category = None
    categories = Category.objects.filter(shop_id=1).order_by('id')
    products = Product.objects.filter(available=True, shop_id=1).order_by('name')
    
    print("[product_list] No. of categories:" , len(categories))
    print("[product_list] No. of products:" , len(products))
    
    #paginator = Paginator(products, 3)
    #page = request.GET.get('page')
    #paged_products = paginator.get_page(page)

    print("category slug:", slug)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.filter(category=category)

    context={'category': category,
                   'categories': categories,
                   'products': products}

    print('Before exiting product_list')


    return render(request,
                  'shop1/list.html',
                  context)


def category_list(request, id, category_slug=None):

    category = None
    #! Display all categories

    # categories = Category.objects.filter(shop_id=1)

    CategoryName = Category.objects.get(id=id)
    
    print("[category_detail] Categories Name:" , CategoryName)

    #! Display all available products
    products = Product.objects.filter(available=True, category_id=id)
    
    #paginator = Paginator(products, 3)
    #page = request.GET.get('page')
    #paged_products = paginator.get_page(page)
    # @ pass database records into listings context
    #context = {'products': paged_products}
    
    print("[category_detail] Categories Name:" , CategoryName)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
                'category': category,
                'products': products,
                'category_name': CategoryName
    }    
    return render(request,
                  'shop1/category.html',
                   context)


def product_detail(request, id, slug):
    
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    category_name = product.category.name  # Access the category name directly
    product_detail_items = ProductDetail.objects.filter(product=product)
    num_items = len(product_detail_items)

    if product_detail_items.exists():
        print("product.name ", product.name)
        print("Number of items in product_detail_items:", num_items)
        print("Categories Name:" , category_name)
    
    d_delivery_date_list = {}
    x = range(2, 14)
    for n in x:
        p_day_01 = datetime.now()
        p_day_n = p_day_01 + timedelta(n)
        d_delivery_date_list[n] = p_day_n.strftime('%Y-%m-%d') + " , " + p_day_n.strftime('%A')
        
        print("Day", n, p_day_n.strftime('%Y-%m-%d'))
        print("Day", p_day_n.strftime('%A'))   

    present_day = datetime.now()
    earliest_date = present_day + timedelta(2)

    print("present_day", present_day.strftime ('%Y-%m-%d'))    
    print("delivery_date.items", d_delivery_date_list)

    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop1/detail.html',
                  {'product': product,
                   'category': category_name,
                   'cart_product_form': cart_product_form,
                   'product_detail_items': product_detail_items,
                   'present_day': present_day,
                   'earliest': earliest_date,
                   'delivery_date': d_delivery_date_list})
    

def ordering(request, id, slug):

    
    if request.method == 'POST':
        
        print('In ordering')

        product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
        
        contact_person = request.POST.get('contact_person', '').strip()
        print('contact person : ', contact_person)
  

        contact_number = request.POST.get('contact_number', '').strip()
        print('contact number : ', contact_number)
        

        contact_email = request.POST.get('contact_email', '').strip()
        print('contact email :', contact_email)

        qty = request.POST.get('qty', '1').strip()  # Get qty from POST data
        print("qty : ", qty)

        if 'cake_size_weight_price' in request.POST:
            cake_size_weight_price = request.POST.get('cake_size_weight_price')
            parts = request.POST.get('cake_size_weight_price').split("/")
            cake_size = parts[0].strip()
            cake_weight = parts[1].strip()
            cake_desc = parts[2].strip()
            cake_price = int(parts[3])
            print("cake_size_weight_price :", cake_size, cake_weight, cake_desc, cake_price)

        if 'pickup_delivery' in request.POST:
            parts = request.POST.get('pickup_delivery').split("/")
            pickup_delivery = parts[0].strip()
            delivery_charges = int(parts[1])

        pickup_delivery_date = request.POST.get('pickup_delivery_date','')
        print("pickup_delivery_date", pickup_delivery_date)


        pickup_delivery_time = request.POST.get('pickup_delivery_time','')
        pickup_delivery_time = pickup_delivery_time.strip()
        print('pickup_delivery_time :', pickup_delivery_time)

        delivery_addr = request.POST.get('delivery_address','')
        delivery_addr = delivery_addr.strip()
        print('delivery_addr :', delivery_addr)

        revised_price = cake_price
        print('revised_price : ', revised_price)  

        ordering_dt = datetime.now()

        product_desc = (
            f"Size {cake_size_weight_price}\n"           
            f"To be delivered on {pickup_delivery_date}"
            f" at {pickup_delivery_time}\n"
            f"Delivery to {delivery_addr}\n"
            f"Contact Person: {contact_person}\n"
            f"Phone Number: {contact_number}   "
            f"Email: {contact_email}\n"
            )     
        print('product_desc :', product_desc)

        cart_product_form = CartAddProductForm(initial={
            'product_desc': product_desc,            # Pass product des description
            'quantity': qty,
            'revised_price' : revised_price
            })
        context = {
            'product': product,
            'product_desc': product_desc,
            'ordering_dt': ordering_dt,
            'ordering_confirm': True,
            'contact_person': contact_person,
            'contact_number': contact_number,
            'contact_email': contact_email,
            'quantity': qty,
            'cake_size': cake_size,
            'cake_weight': cake_weight,
            'cake_desc': cake_desc,
            'cake_price': cake_price,
            'pickup_delivery': pickup_delivery,
            'pickup_delivery_time': pickup_delivery_time,
            'pickup_delivery_date': pickup_delivery_date,
            'delivery_addr': delivery_addr,
            'delivery_charges': delivery_charges,
            'revised_price': revised_price,
            'cart_product_form': cart_product_form
            }  
 
    return render(request,
                  'shop1/ordering.html',
                  context)
                   