#from celery import shared_task
from django.core.mail import send_mail
from .models import Order


# from celery import shared_task

# @shared_task
def send_mail(order_id):
     """

    Task to send an e-mail notification when an order is
    successfully created.
    """
     """
order = Order.objects.get(id=order_id)
subject = f'Order nr. {order.id}'
message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    


def send_welcome_email(user_email):
    subject = 'Welcome to My Site'
    message = 'Thank you for signing up for our site!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

    """