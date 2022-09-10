from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from courses.models import Course
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe



stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def checkout(request):

    context = {
        'stripe_key':settings.STRIPE_PUBLIC_KEY,
    }
    return render(request,'purchase/checkout.html',context)



YOUR_DOMAIN = 'http://localhost:8000'


@csrf_exempt
def create_checkout_session(request,pk=18):
    course = get_object_or_404(Course,pk=pk)
    print(YOUR_DOMAIN+course.picture.url)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(course.price*100),
                        'product_data': {
                            'name': course.title,
                             # 'images': [YOUR_DOMAIN+course.picture.url],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": course.id
            },
            mode='payment',
            success_url='/courses/addstudent/'+str(course.slug),
            cancel_url=f'/{course.slug}/',
        )
        return JsonResponse(
            {
                'sessionId' : session.id,
                'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
            }
        )
    except Exception as e:
        print(str(e))

    return redirect('/')



