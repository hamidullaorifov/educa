from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from courses.models import Course
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import datetime
import stripe
import json



stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def checkout(request,pk):
    course = get_object_or_404(Course,pk=pk)
    context = {
        'stripe_key':settings.STRIPE_PUBLIC_KEY,
        'course':course,
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
            expires_at=int(datetime.datetime.now(datetime.timezone.utc).timestamp()+5),
            customer_email=request.user.email,
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
            # success_url='https://rapidapi.com/',
            success_url='/courses/addstudent/'+str(course.slug),
            cancel_url=f'/{course.slug}/',
            # cancel_url=f'https://rapidapi.com/',
        )
        print(session)
        return JsonResponse(
            {
                'sessionId' : session.id,
                'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
            }
        )
    except Exception as e:
        print(str(e))

    return redirect('/')


@csrf_exempt
def create_payment_intent(request,pk):
    print(pk)
    try:
        customer = stripe.Customer.create(email=request.user.email)
        course = Course.objects.get(pk=pk)
        intent = stripe.PaymentIntent.create(
            amount=int(100*course.price),
            currency='usd',
            customer=customer['id'],
            metadata={
                "product_id": course.id
            },
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(e)
        return JsonResponse({ 'error': str(e) })
@csrf_exempt
def confirm_payment_intent(request):
    if request.method=='POST':
        data = json.loads(request.body)
        payment_intent = stripe.PaymentIntent.modify(
            data['clientSecret'],
            payment_method=stripe.PaymentMethod.create(
            type = "card",
            card = data['card']
            )
        )
