from .models import Comment
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course,Rating
from django.conf import settings

import stripe
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY
def home(request):
    courses = Course.objects.all()[:8]
    context = {
        'courses':courses,
    }
    return render(request,'courses/index.html',context)


def course_detail(request,slug):
    # need caching
    my_rate=None
    course = get_object_or_404(Course,slug=slug)
    try:
        my_rate = Rating.objects.get(course=course,author=request.user).star
    except:
        pass
    rates = Rating.objects.filter(course=course)
    # if request.user:
    #     rates = rates.exclude(user=request.user)
    rates_list=[]
    if rates:
        rates_list = [
            {
                'author':rate.author,
                'feedback':rate.feedback,
                'stars':range(rate.star),
                'nostars':range(rate.star,5),

        }for rate in rates
        ]
    


    ###########################################################################
    # session = stripe.checkout.Session.create(
    #    payment_method_types=['card'],
    #         line_items=[
    #             {
    #                 'price_data': {
    #                     'currency': 'usd',
    #                     'unit_amount': int(course.price*100),
    #                     'product_data': {
    #                         'name': course.title,
    #                         # 'images': ['https://i.imgur.com/EHyR2nP.png'],
    #                     },
    #                 },
    #                 'quantity': 1,
    #             },
    #         ],
    #         metadata={
    #             "product_id": course.id
    #         },
       
    #     mode='payment',
    #     success_url='https://github.com/',
    #     cancel_url='https://www.google.com/',
    # )

    #############################################################################
    context = {
        'course':course,
        'myrate':my_rate,
        'rates':rates_list,
        # 'session_id':session.id,
        'stripe_public_key':settings.STRIPE_PUBLIC_KEY, 
        
    }
    return render(request,'courses/course-details.html',context)


@login_required
def post_comment(request,pk):
    if request.method == 'POST':
        course = get_object_or_404(Course,pk=pk)
        print(request.POST)
        content = request.POST['message']
        Comment.objects.create(
            course=course,
            author=request.user,
            content=content
        )
        return redirect(course.get_absolute_url())

@login_required
def post_feedback(request,pk):
    if request.method == 'POST':
        course = get_object_or_404(Course,pk=pk)
        data = request.POST
        rating,created = Rating.objects.get_or_create(course=course,author=request.user)
        rating.star =int(data['rating'])
        rating.feedback = data['feedback']
        rating.save()
        return redirect(course.get_absolute_url())