from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
# from contacts.models import Contact
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from django.db.models import Sum

User = get_user_model()

# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password= password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now logged in ')
            return redirect('accounts:dashboard')
            print('Login successful')        
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')

        return redirect('accounts:login')
    else:
        return render(request,'accounts/login.html')



def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username already exists')
                return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email is already used")
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username = username, 
                        password=password, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
                    user.save()
                    messages.success(request,'You are now registered and can log in')
                    print('register successfully')
                    return render(request, 'accounts/login.html')
                
                #render(request,'accounts/login.html')
        else:
            messages.error(request, "password not match")
            return redirect('accounts:register')
    else:        
        return render(request, 'accounts/register.html')
    
        
    

def logout(request):
    if request.method == 'POST':
            auth.logout(request)
#            messages.success(request, 'You are now logged out')
            return redirect('shop:index')


def dashboard(request):

    order_items = None
    username = None
    email = None
    registered_date = None
    first_name = None
    last_name = None
    phone_number = None

    current_user = request.user
    
    # Check if the user is authenticated
    if current_user.is_authenticated:
        username = current_user.username  # Get the username
        email = current_user.email  # Get the email
        registered_date = current_user.date_joined  # Get the registered date
        first_name = current_user.first_name
        last_name = current_user.last_name
        phone_number = current_user.phone_number
        order_items = OrderItem.objects.filter(
            username=current_user.username).order_by('-order_id')
        # Calculate the total of total_item_price
        total_price = order_items.aggregate(Sum('total_item_price'))['total_item_price__sum'] or 0

    else:
        username = None  # Or handle the case where the user is not authenticated
        order_items = None
    context = {
        'order_items': order_items,
        'username': username,
        'email': email, 
        'registered_date': registered_date,
        'first_name' : first_name, 
        'last_name' : last_name, 
        'phone_number': phone_number,
        'total_price': total_price

    }
    print('username:', username, 'email:', email, 'registered_date:', 
          registered_date, 'first_name:', first_name, 'last_name:', last_name, 'phone_number:', phone_number)
    
    return render(request, 'accounts/dashboard.html', context)


