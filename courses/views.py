from .models import Comment
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from courses.models import Course,Rating

# Create your views here.

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
    rates = Rating.objects.filter(course=course).exclude(author=request.user)
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