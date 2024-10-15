import weasyprint
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
#from .tasks import order_created



from django.contrib.auth.models import User

# from contacts.models import Contact
from django.contrib.auth import get_user_model

def order_create(request):
    cart = Cart(request)
    username = ''
    total_item_price = 0
    current_user = request.user
    if current_user.is_authenticated:
        username = current_user.username  # Get the username

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                print("product id: " + str(item['product'].id))
                print("product desc: " + str(item['product_desc']))
                print("price: " + str(item['price']))
                print("quantity: " + str(item['quantity']))
                # Calculate total item price
                total_item_price = item['price'] * item['quantity']
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         product_desc=item['product_desc'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         studio_name=item['studio_name'],
                                         # date=item['date'],
                                         
                                         # time_slot=item['time_slot'],
                                         guests=item['guests'],
                                         username=username,
                                         total_item_price= total_item_price,
                                         )
                
                print("date: " + str(item['date']))
                print("time_slot: " + str(item['time_slot']))
                
            # clear the cart
            
            print ("cart cleared - order id: " + str(order.id)) 
            subject = f'Order nr. {order.id}'
            message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
            # send_mail(subject,
              #            message,
               #           'admin@myshop.com',
                #          [order.email])
            
            # print('send email order id ' + str(order.id)+ ' to ' + order.email)
           
            return redirect(reverse('payment:process') + f'?order_id={order.id}')
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/admin/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + '/css/pdf.css')])
    return response
