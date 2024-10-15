import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datetime import datetime 
from orders.models import Order, OrderItem
#from .tasks import payment_completed
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import weasyprint
from django.template.loader import render_to_string
from io import BytesIO
from cart.cart import Cart
from smtplib import SMTPException
from socket import timeout  # Import timeout from socket module

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def send_order_confirmation(order):
    print('Order ID: ' + str(order.id))
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed an order.\n'
        f'Your order ID is {order.id}.'
    )
    
    email_address = order.email
    print('Email address: ' + email_address)

    # Create the email message
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='admin@myshop.com',
        to=[email_address],
    )
    
    print('Email message ready')

        
# generate PDF
    html = render_to_string('orders/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    
    # write the pdf to media directory
    with open(settings.MEDIA_ROOT+'/invoices/order_' + str(order.id) + '.pdf', 'wb') as f: f.write(out.getvalue())

    print(f'{datetime.now():%Y-%m-%d %H:%M:%S} - PDF attachment ready')
    
    # Attach the file
    email.attach(settings.MEDIA_ROOT +f'/invoices/order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf')

    
    #email.attach_file(file_path)

    print('Just before sending email')
    # Send the email
    try:
        email.send()
        print('Order confirmation email sent successfully.')
    except timeout:
        print('Email sending timed out. Please try again later.')
        # Handle timeout (e.g., log the error, notify the user, etc.)
    except SMTPException as e:
        print(f'Failed to send email: {str(e)}')
        # Handle other SMTP errors (e.g., log the error, notify the user, etc.)
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        # Handle any other unexpected errors

    print('email sent - email ID ' + order.email + str(order.id))

def payment_process(request):
    cart = Cart(request)
    order_id = request.GET.get('order_id')

    print('payment_process - order id: ' + order_id)

    if order_id:
        order = get_object_or_404(Order, id=order_id)
        # Process the payment using the order object
    else:
        print('Order processing error - cannot retrieve back record order id' + order_id)

    total_cost = order.get_total_cost()

    print('Enter payment_process - order id: ' + str(order_id))

    if request.method == 'POST':

        # retrieve nonce
        print('POST data request.POST = ', request.POST)
        nonce = request.POST.get('payment_method_nonce', None)
        print( 'nonce: ' + nonce)

        # create and submit transaction to braintree
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        
        if result.is_success:
            # mark the order as paid
            print('Payment result ok: ' + str(order.id))
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            print('result.transaction.id: ' + result.transaction.id)

            # save the order on status of payment
            order.save()
            # clear the cart
            cart.clear()
            print ("cart cleared - order id: " + str(order.id)) 
            send_order_confirmation(order)
            return redirect('payment:done')
        
        else:           
            # Log the error details
            print('Payment result failed for order ID: ' + str(order.id))
            print('Error Message: ' + result.message)

            return render(request,
            'payment/canceled.html',
            {'error_message': result.message},)
            
            # return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
            'payment/process.html',
            {'order': order,
            'client_token': client_token,
            'cart': cart,
            },)


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

from django.core.mail import EmailMessage


