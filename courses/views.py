import json
from .models import Comment
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course,Rating,Content
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
import stripe
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY
def home(request):
    courses = Course.objects.all()
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
    



    context = {
        'course':course,
        'myrate':my_rate,
        'rates':rates_list,
        'stripe_public_key':settings.STRIPE_PUBLIC_KEY, 
        
    }
    return render(request,'courses/course-details2.html',context)


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
    
@login_required
def course_content(request,pk=1):
    content = get_object_or_404(Content,pk=pk)
    course = content.module.course
    if request.user in course.students.all():
        context = {
            'content':content,
        }
        print(content)
        return render(request,'courses/course-content.html',context=context)
    else:
        return redirect(course.get_absolute_url())


@csrf_exempt
@login_required
def add_user_to_students(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course = get_object_or_404(Course,id=data['id'])
        course.students.add(request.user)
        content = course.modules.first().contents.first()
        print(content)
        return JsonResponse({
            "url":"/courses/content/"+str(content.pk)
        })
    return JsonResponse({
        'url':"",
    })