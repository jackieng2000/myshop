from django.db import models
from shop.models import Product
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_hour(value):
        if value < 0 or value > 23:
            raise ValidationError('Hour must be between 0 and 23.')

class Order(models.Model):
    id = models.AutoField(primary_key=True) # #key
    shop_id = models.IntegerField(default=4)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

    # added on 2024/09/21
    # for linking registered user
    username = models.CharField(default="", max_length=150, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):



    CHOICES_NO_OF_GUESTS = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
    ]

    id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField(default=1)

    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # added on 2024/09/21
    studio_name = models.CharField(max_length=200, null=True, blank=True, default="")
    booking_date= models.DateTimeField(null=True, blank=True,default=timezone.now)
    guests = models.PositiveIntegerField(null=True, blank=True, default=0)  # Ensures guests can't be negative
    # time_slot = models.TimeField()  # Uncomment if needed
    lasting_hours = models.PositiveIntegerField(null=True, blank=True, default=0)  # Renamed for clarity

    product_desc = models.TextField(default="",blank=True, max_length=200)

    # for linking registered user
    username = models.CharField(default="", max_length=150, blank=True)
    related_order_id = models.PositiveIntegerField(null=True, blank=True, default=0)

    total_item_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)    

    contact_person = models.CharField(max_length=50, null=True)
    contact_number = models.CharField(max_length=50,default=None, blank=True, null=True)
    contact_email = models.CharField(max_length=50, default=None, blank=True, null=True)
    cake_size = models.CharField(max_length=50, default=None, blank=True, null=True)
    cake_weight = models.CharField(max_length=50, default=None, blank=True, null=True)
    cake_desc = models.CharField(max_length=50, default=None, blank=True, null=True)
    cake_price = models.IntegerField(default=0, blank=True, null=True)
    pickup_delivery = models.CharField(max_length=100, default=None, blank=True, null=True)
    pickup_delivery_time = models.CharField(max_length=50, default=None, blank=True, null=True)
    pickup_delivery_date = models.CharField(max_length=50, default=None, blank=True, null=True)
    delivery_addr = models.CharField(max_length=500, default=None, blank=True, null=True)
    delivery_charges = models.IntegerField(default=0, blank=True, null=True)
    order_amount = models.IntegerField(default=0, blank=True, null=True)

    # Define the validation function
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
