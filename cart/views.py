from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from decimal import Decimal


@require_POST
def cart_add(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_id = product.shop_id
    print('Entering cart_add')
    print('Product Shop ID :', shop_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        print('product_desc :' + cd['product_desc'])

        print('product_id: ' + str(product_id))
        print('quantity: ' + str(cd['quantity']))
        


        if shop_id == 1 :
            cart.add(product=product,
                 quantity=cd['quantity'],
                 product_desc= cd['product_desc'],   # add product description or other field
                 override_quantity=cd['override'],
                 revised_price = float(cd['revised_price'])                
                 )
            
            print('revised_price :', cd['revised_price'] )
            print('cart shop 1 transaction added :', cd['product_desc'] )

        if shop_id == 2 :
            cart.add(product=product,
                 quantity=cd['quantity'],
                 product_desc= cd['product_desc'],   # add product description or other field
                 override_quantity=cd['override'],
                 revised_price = float(product.price)                 
                 )
            print('cart shop 2 transaction added : ', cd['product_desc'] )

        if shop_id == 3 :

            date=request.POST.get('date')
            guests = request.POST.get('guests')
            time_slot = request.POST.get('time_slot')
            studio_name = request.POST.get('studio_name')
            format_product_desc = (
                            f"{product.name}\n"
                            f"{studio_name}\n"
                            f"{date}\n"
                            f"{time_slot}\n"
                            f"Guest(s):{guests}\n"
                        
                            )
            
            cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'],            
                product_desc = format_product_desc,
                revised_price = float(product.price),   
                date=date,
                guests=guests,
                time_slot=time_slot,
                studio_name=studio_name,
                )
            
            print('shop 3 Cart transaction added :' , format_product_desc )

        if shop_id == 4 :
            cart.add(product=product,
                 quantity=cd['quantity'],
                 product_desc= product.description,   # add product description or other field
                 override_quantity=cd['override'],
                 revised_price = float(product.price)                    
                 )
            print('cart shop 4 transaction added :' , product.name)
        
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
       item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'product_desc': item['product_desc'],
                                                                   'override': True, 'revised_price': Decimal(item['price'])})
    return render(request, 'cart/detail.html', {'cart': cart})
