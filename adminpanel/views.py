from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course, Module,Content
from .forms import CourseForm,ModuleForm,ContentForm
from django.http import JsonResponse
from .utils import owner_required,check_owner
from django.http import HttpResponseForbidden

# Create your views here.
@login_required
def my_courses(request):
    user = request.user
    my_courses = Course.objects.filter(owner=user)

    context = {
        'my_courses':my_courses
    }
    return render(request,'adminpanel/mycourses.html',context)

@login_required
def create_coure(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST,files=request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            # course.picture = request.FILES['picture']
            course.save()
            return redirect('mycourses')
        else:
            form.errors = "Form is not valid"
    return render(request,'adminpanel/course-create.html',{'form':form})

@login_required
def edit_course(request,pk):
    course = Course.objects.get(pk=pk)
    if not course.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    form = CourseForm(instance=course)
    if request.method =='POST':
        form = CourseForm(request.POST,files=request.FILES,instance=course)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.owner = request.user
            new_course.save()
            return redirect('mycourses')
        else:
            form.add_error(error="ValidationError")
    return render(request,'adminpanel/course-edit.html',{'form':form})


@login_required
def delete_course(request,pk):
    if request.method == 'POST':
        course = Course.objects.get(pk=pk)
        if not course.owner == request.user:
            return HttpResponseForbidden("<h1>You are not allowed</h1>")
        course.delete()
        return redirect('mycourses')
    return render(request,'adminpanel/course-delete.html')

@login_required
def course_modules(request,pk):
    course = get_object_or_404(Course,pk=pk)
    if not course.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    context = {
        'course':course
    }
    return render(request,'adminpanel/course-modules.html',context)


@login_required
def get_module_contents(request,pk):
    module = get_object_or_404(Module,pk=pk)
    if not module.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    contents = [
        {
            'pk':content.pk,
            'title':content.title,
        }
        for content in module.contents.all()
    ]
    return JsonResponse({
        'contents':contents,
        'title':module.title,
        'description':module.description,
    })



@login_required
def create_module(request,slug):
    course = get_object_or_404(Course,slug=slug)
    if not course.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")

    
    form = ModuleForm()
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            new_module = form.save(commit=False)
            new_module.course = course
            new_module.save()
            return redirect('course-modules',pk=course.pk)
        else:
            form.add_error('title',error=ValidationError())
    return render(request,'adminpanel/create-module.html',{'form':form})


@login_required
def update_module(request,id):
    module = get_object_or_404(Module,pk=id)
    if not module.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    form = ModuleForm(instance=module)
    if request.method == 'POST':
        form = ModuleForm(request.POST,instance=module)
        if form.is_valid():
            new_module = form.save()
            return redirect('course-modules',pk=module.course.pk)
        else:
            form.add_error('title',error=ValidationError())
    return render(request,'adminpanel/update-module.html',{'form':form})

@login_required   
def delete_module(request,id):
    module = get_object_or_404(Module,pk=id)
    if not module.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    course = module.course
    if request.method=='POST':
        module.delete()
        return redirect('course-modules',pk=course.pk)
    return render(request,'adminpanel/delete-module.html',{'course':course})



@login_required
def create_content(request,pk):
    module = get_object_or_404(Module,pk=pk)
    if not module.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    form = ContentForm()
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            new_content = form.save(commit=False)
            new_content.module = module
            new_content.save()
            return redirect('course-modules',pk=module.course.pk)
        else:
            form.add_error('title',error=ValidationError())
    return render(request,'adminpanel/create-content.html',{'form':form})




@login_required
def update_content(request,id):
    content = get_object_or_404(Content,pk=id)
    if not content.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    form = ContentForm(instance=content)
    if request.method == 'POST':
        form = ContentForm(request.POST,instance=content)
        if form.is_valid():
            new_content = form.save()
            return redirect('course-modules',pk=content.module.course.pk)
        else:
            form.add_error('title',error=ValidationError())
    return render(request,'adminpanel/update-content.html',{'form':form})


@login_required   
def delete_content(request,):
    content = get_object_or_404(Content,pk=id)
    if not content.owner == request.user:
        return HttpResponseForbidden("<h1>You are not allowed</h1>")
    course = content.module.course
    if request.method=='POST':
        content.delete()
        return redirect('course-modules',pk=course.pk)
    return render(request,'adminpanel/delete-content.html',{'course':course})


def forbidden(request):
    return HttpResponseForbidden("You are not allowed")