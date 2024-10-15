from django.shortcuts import render, get_object_or_404
from django.db.models import F  
from cart.forms import CartAddProductForm
from shop.models import Category, Product
from .models import Instructor
from django.shortcuts import render
from django.http import JsonResponse
from .models import MenuItem, Instructor, CourseSession
from django.db.models import F, ExpressionWrapper, IntegerField

def product_list(request):
    # Fetch all available MenuItem records
    menu_items = MenuItem.objects.filter(available=True)
    
    # Fetch all available Instructor records
    instructors = Instructor.objects.filter(available=True)

    # Render the template with the menu items and instructors
    return render(request, 'shop2/list.html', {
        'menu_items': menu_items,
        'instructors': instructors,
    })
def available_course_sessions(request):
    # Fetch course sessions where quota is greater than or equal to filled places
    course_sessions = CourseSession.objects.filter(available=True, quota__gte=F('filled_place')).annotate(
        available_places=ExpressionWrapper(
            F('quota') - F('filled_place'),
            output_field=IntegerField()
        )
    )
    return render(request, 'shop2/registration.html', {
        'course_sessions': course_sessions,
    })

def product_detail(request, id, slug):
    courses_sessions = get_object_or_404(CourseSession,
                                id=id,
                                slug=slug,
                                available=True)
    print('courses_sessions : ', courses_sessions)
    print('courses_sessions.product_id : ', courses_sessions.product_id)
    product = get_object_or_404(Product,
                                name=courses_sessions.product_id,)
    print('product : ', product)
    

    # Construct product description with line breaks
    formatted_start_date_time = courses_sessions.start_date_time.strftime('%d-%b-%y %H:%M')

    # Construct product description with line breaks
    product_desc = (
        f"{courses_sessions.name}\n"
        f"{courses_sessions.instructor.name}\n"
        f"{courses_sessions.location}\n"
        f"{formatted_start_date_time}"
    )
    
    cart_product_form = CartAddProductForm(initial={
        'product_desc': product_desc,            # Pass product des description
    })
    return render(request,
                  'shop2/detail.html',
                  {'product': product, 
                   'cart_product_form': cart_product_form})

