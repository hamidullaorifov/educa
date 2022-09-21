from courses.models import Course,Module,Content
from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponseForbidden
from django.urls import reverse

def owner_required(Klass=Course):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            if 'id' in kwargs:
                obj = get_object_or_404(Klass,pk=kwargs['id'])
            elif 'slug' in kwargs:
                obj = get_object_or_404(Klass,slug=kwargs['slug'])
            else:
                obj = get_object_or_404(Klass,slug=kwargs['slug'])
            if obj.owner == request.user:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponseForbidden("Forbidden")
        return wrapper_func
    return decorator



def check(view_func):
    def wrapper_func(obj,request):
        print("owner",obj.owner)
        print("user",request.user)
        if not request.user == obj.owner:
            print("Forbidden")
            return redirect("forbidden")
        else:
            view_func(obj,request)
    return wrapper_func




def check_owner(obj,request):
    def check():
        if obj.owner==request.user:
            pass
        else:
            return HttpResponseForbidden("Your access forbiddennn")
    return check