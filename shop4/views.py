from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from shop.models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(shop_id=4)
    products = Product.objects.filter(available=True,shop_id=4)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category,available=True,shop_id=4)
    return render(request,
                  'shop4/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    product_desc = product.description
    cart_product_form = CartAddProductForm(initial={
        'product_desc': product_desc,            # Pass product des description
    })
    return render(request,
                  'shop4/detail.html',
                  {'product': product, 
                   'cart_product_form': cart_product_form})
