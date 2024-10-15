import calendar
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddProductForm
from shop.models import Category, Product
from shop1.models import ProductDetail, Ordering
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from datetime import datetime, timedelta
from .forms import Create_Ordering
from django.utils import timezone

#<Hard Code Table> from listings.choices import price_choices, bedroom_choices, district_choices
#!
#@

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all().order_by('id')
        
    #! Display all available products
    #listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    #products = Product.objects.filter(available=True)[:Number of records display]
    products = Product.objects.filter(available=True).order_by('-name')
    
    print("[product_list] No. of categories:" , len(categories))
    print("[product_list] No. of products:" , len(products))
    
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # @ pass database records into listings context
 
    context = {
                'category': category,
                'products': products,
                'categories': categories,
    }
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop1/product/list.html',
                  context)
                  #{'category': category,
                  #'categories': categories,
                  #'products': products},)

def category_list(request, id, category_slug=None):
    category = None
    #! Display all categories
    categories = Category.objects.all()
    CategoryName = Category.objects.get(id=id)
    
    print("[category_detail] Categories Name:" , CategoryName)

    #! Display all available products
    #listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    #products = Product.objects.filter(available=True)[:Number of records display]
    products = Product.objects.filter(available=True, category_id=id)
    
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # @ pass database records into listings context
    #context = {'products': paged_products}
    
    print("[category_detail] Categories Name:" , CategoryName)
    
    context = {
                'category': category,
                'products': products,
                'category_name': CategoryName
    }
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop1/product/category.html',
                   context)


def product_detail(request, id, category_id):
    
    product = get_object_or_404(Product,
                                id=id,
                                category_id=category_id,
                                available=True)
    
    CategoryName = Category.objects.get(id=category_id)
    
    ProductDetail_Item = ProductDetail.objects.filter(product_id_id=id).values()
    if ProductDetail.objects.filter(product_id_id=id).exists():
        print("[product_detail] ProductDetail_Item:" , ProductDetail_Item)
        #ProductDetail_Item    
        
    print("[product_detail] Categories Name:" , CategoryName)
    
    cart_product_form = CartAddProductForm()
   
    dDeliveryDateList = {}
    x = range(2, 14)
    for n in x:
        pday01 = datetime.now()
        pdayN = pday01 + timedelta(n)
        dDeliveryDateList[n] = pdayN.strftime('%Y-%m-%d')
        print("Day", n, pdayN.strftime('%Y-%m-%d'))   

    presentday = datetime.now()
    fastest = presentday + timedelta(2)
    
    print("presentday", presentday.strftime ('%Y-%m-%d'))    
    print("DeliveryDate.items", dDeliveryDateList)

    return render(request,
                  'shop1/product/detail.html',
                  {'product': product,
                   'category': CategoryName,
                   'cart_product_form': cart_product_form,
                   'ProductDetail_Item': ProductDetail_Item,
                   'presentday': presentday.strftime ('%Y-%m-%d'), #Today
                   'fastest': fastest.strftime('%Y-%m-%d'),
                   'DeliveryDate': dDeliveryDateList})
    
def ordering(request, id, category_id):
    print("ordering: [request.POST]" , request.POST) 
    
    if request.method == 'POST':
        form = Ordering(request.POST)
        
        if 'ContactPerson' in request.POST:
            ContactPerson = request.POST.get('ContactPerson')
            ContactPerson = ContactPerson.strip()
        if 'ContactNumber' in request.POST:
            ContactNumber = request.POST.get('ContactNumber')
            ContactNumber = ContactNumber.strip()
        if 'ContactEmail' in request.POST:
            ContactEmail = request.POST.get('ContactEmail')
            ContactEmail = ContactEmail.strip()
        if 'Qty' in request.POST:
            Qty = int(request.POST.get('Qty'))
        if 'CakeSizeWeightPrice' in request.POST:
            input_string = request.POST.get('CakeSizeWeightPrice')
            parts = input_string.split("/")
            CakeSize = parts[0]
            CakeSize = CakeSize.strip()
            CakeWeight = parts[1]
            CakeWeight = CakeWeight.strip()
            CakeDesc = parts[2]
            CakeDesc = CakeDesc.strip()
            CakePrice = int(parts[3])
        if 'PickupDelivery' in request.POST:
            input_string = request.POST.get('PickupDelivery')
            parts = input_string.split("/")
            PickupDelivery = parts[0]
            PickupDelivery = PickupDelivery.strip()
            DeliveryCharges = int(parts[1])
        if 'PickupDeliveryDate' in request.POST:
            dDeliveryDateList = {}
            x = range(2, 14)
            for n in x:
                pday01 = datetime.now()
                pdayN = pday01 + timedelta(n)
                dDeliveryDateList[n] = pdayN.strftime('%Y-%m-%d')
            PickupDeliveryDate = dDeliveryDateList[request.POST.get('PickupDeliveryDate')] = pdayN.strftime('%Y-%m-%d')  
        if 'PickupDeliveryTime' in request.POST:
            PickupDeliveryTime = request.POST.get('PickupDeliveryTime')
            PickupDeliveryTime = PickupDeliveryTime.strip()
        if 'DeliveryAddress' in request.POST:
            DeliveryAddr = request.POST.get('DeliveryAddress')  
            DeliveryAddr = DeliveryAddr.strip()
        Amount = (int(Qty) * int(CakePrice)) + int(DeliveryCharges)   
        Product_id = int(id)
        Category_id = int(category_id)
        #CurrentDateTime = datetime.now()
        #OrderingDT = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        #OrderingDT = timezone.localtime(timezone.now()) # Get the current local datetime
        # now = datetime.now()
        # now_string = now.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
        # OrderingDT = datetime.strptime(now_string, "%Y-%m-%d %H:%M:%S")
        OrderingConfirm = False
        
        context = {
            #'OrderingDT': OrderingDT,
            #'OrderingConfirm': False,
            'ContactPerson': ContactPerson,
            'ContactNumber': ContactNumber,
            'ContactEmail': ContactEmail,
            'Qty': Qty,
            'CakeSize': CakeSize,
            'CakeWeight': CakeWeight,
            'CakeDesc': CakeDesc,
            'CakePrice': CakePrice,
            'PickupDelivery': PickupDelivery,
            'PickupDeliveryTime': PickupDeliveryTime,
            'PickupDeliveryDate': PickupDeliveryDate,
            'DeliveryAddr': DeliveryAddr,
            'DeliveryCharges': DeliveryCharges,
            'OrderAmount': Amount,
            'Product_id': Product_id,
            'Category_id': Category_id
            }

    print(" ---context---:", context)
    
    form = Create_Ordering(context)
    
    print("form.is_valid()", form.is_valid())
    if form.is_valid():
        print("//form.is_valid //" ,context) 
        #form.save()  # Save the form data to the database 
        
        new_order = Ordering.objects.create(
                    ContactPerson = ContactPerson,
                    ContactNumber = ContactNumber,
                    ContactEmail = ContactEmail,
                    Qty = Qty,
                    CakeSize = CakeSize,
                    CakeWeight = CakeWeight,
                    CakeDesc = CakeDesc,
                    CakePrice = CakePrice,
                    PickupDelivery = PickupDelivery,
                    PickupDeliveryTime = PickupDeliveryTime,
                    PickupDeliveryDate = PickupDeliveryDate,
                    DeliveryAddr = DeliveryAddr,
                    DeliveryCharges = DeliveryCharges,
                    OrderAmount = Amount,
                    Product_id = Product_id,
                    Category_id = Category_id,
                    Session_Key = request.session.session_key)
        new_order_id = new_order.id  # Get the ID of the newly created record
            
        print("---New Ordering ID--- ",new_order_id)
        print("session_id:", request.session.session_key)
            
        Msg = "Add to the cart!"

        RecordCreated = True
        
        #return redirect('success')  # Redirect after saving
        
        if 'Msg' in locals():
            print("'Msg' in locals()", 'Msg' in locals())
            if Msg is not None:
                queryset_list = Ordering.objects.order_by('-OrderingDT')
                if request.session.session_key:
                    queryset_list = queryset_list.filter(
                        Session_Key__iexact=request.session.session_key
                    )
                    
            return render(request,
                  'shop1/product/ordering.html',{
                  'ContactPerson': ContactPerson,
                  'ContactNumber': ContactNumber,
                  'ContactEmail': ContactEmail,
                  'Qty': Qty,
                  'CakeSize': CakeSize,
                  'CakeWeight': CakeWeight,
                  'CakeDesc': CakeDesc,
                  'CakePrice': CakePrice,
                  'PickupDelivery': PickupDelivery,
                  'PickupDeliveryTime': PickupDeliveryTime,
                  'PickupDeliveryDate': PickupDeliveryDate,
                  'DeliveryAddr': DeliveryAddr,
                  'DeliveryCharges': DeliveryCharges,
                  'OrderAmount': Amount,
                  'Product_id': Product_id,
                  'Category_id': Category_id,
                  'Session_Key': request.session.session_key,
                  'new_order_id': new_order.id,
                  'Msg': Msg,
                  'Orderings': queryset_list,
                  'total' : len(queryset_list)})        
    else:
        print("Form errors:", form.errors)  # This will show you the validation errors
        form = Ordering()
    
    #return render(request, 'shop1/product/ordering.html', {'form': form})