import logging
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from shop.models import Category, Product
from .models import Studio, Booking
from datetime import datetime, timedelta
from django.http import JsonResponse

def product_list(request, category_slug=None):
    context = {}
    
    # Initialize variables
    studio_name = None
    booking_date = None
    guests = None
    time_slot = None

    if request.method == 'POST':
        studio_id = request.POST.get('studio')
        studio = get_object_or_404(Studio, id=studio_id)

        studio_name = studio.name
        booking_date = request.POST.get('date')
        guests = request.POST.get('guests')
        time_slot = request.POST.get('time_slot')

        context.update({
            'studio_name': studio.name,
            'studio_district': studio.district,   
            'date': request.POST.get('date'),
            'guests': request.POST.get('guests'),
            'time_slot': request.POST.get('time_slot'),
        })
        print('In product_list')
        print('studio_name:', studio_name)
        print('date:',booking_date )
        print('guests:', guests)
        print('time_slot:', time_slot)
    
    category = None
    categories = Category.objects.filter(shop_id=3)
    products = Product.objects.filter(available=True, shop_id=3)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        print('date : ', booking_date )
    
    context.update({
        'category': category,
        'categories': categories,
        'products': products,
        'date': booking_date,             
        'guests':guests,
        'time_slot':time_slot,
        'studio_name':studio_name,
    })
    
    return render(request, 'shop3/list.html', context)

def baking_studio(request):
    return render(request, 'shop3/baking_studio.html')

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    date=request.POST.get('date')
    guests = request.POST.get('guests')
    time_slot = request.POST.get('time_slot')
    studio_name = request.POST.get('studio_name')

    print('In product_detail')
    print('product:', product)
    print('date:', date)
    print('guests:', guests)
    print('time_slot:', time_slot)
    print('studio_name:', studio_name)
    
    cart_product_form = CartAddProductForm(initial={
        'product_desc': product.description,  # Assuming 'description' is a field in your Product model
        'studio_name': studio_name,   # Assuming 'studio' is a related field in your Product model
        'quantity': 1,  # Default quantity
        })

    return render(request, 'shop3/detail.html',
                   {'date':date, 
                    'guests':guests,
                    'time_slot':time_slot,
                    'studio_name': studio_name,
                    'product': product, 
                    'cart_product_form': cart_product_form})

#logger = logging.getLogger(__name__)


def booking(request):
    studios = Studio.objects.all()
    return render(request, 'shop3/booking.html', {'studios': studios})

def check_availability(request):
    studio_id = request.GET.get('studio_id')
    date = request.GET.get('date')
    guests = int(request.GET.get('guests'))

    studio = get_object_or_404(Studio, id=studio_id)
    date = datetime.strptime(date, '%Y-%m-%d').date()

    available_slots = []
    start_time = datetime.strptime('10:00', '%H:%M').time()
    end_time = datetime.strptime('19:00', '%H:%M').time()
    session_duration = timedelta(hours=3)

    current_time = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)

    while current_time + session_duration <= end_datetime:
        slot_start_time = current_time.time()
        slot_end_time = (current_time + session_duration).time()

        bookings = Booking.objects.filter(
            studio=studio,
            date=date,
            start_time__lt=slot_end_time,
            end_time__gt=slot_start_time
        )

        total_booked = sum(booking.guests for booking in bookings)
        available_capacity = studio.capacity - total_booked

        if available_capacity >= guests:
            available_slots.append({
                'start_time': slot_start_time.strftime('%H:%M'),
                'end_time': slot_end_time.strftime('%H:%M')
            })

        current_time += timedelta(hours=1)

    return JsonResponse({'available_slots': available_slots})

