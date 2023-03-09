from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from courses.models import CustomUser

def login_view(request):
    context={}
    if request.method == 'POST':
        data = request.POST
        username=data['username']
        # email=data['email']
        password=data['pass']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user=user)
            return redirect('/')
        context={
            'message':'Invalid credentials',
        }
    return render(request,'accounts/login.html',context)

def sign_up(request):
    if request.method == 'POST':
        data = request.POST
        username=data['username']
        email=data['email']
        firstname=data['firstname']
        lastname=data['lastname']
        password=data['pass']
        if CustomUser.objects.filter(username=username).exists():
            return render(request,'accounts/signup.html',{'message':'This username already in use'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request,'accounts/signup.html',{'message':'This email already in use'})
        user = CustomUser.objects.create_user(
          username=username,
          email=email,
          first_name=firstname,
          last_name=lastname,
          password=password,
          role='student' 
        )
        login(request,user)
        return redirect('/')
    return render(request,'accounts/signup.html')


# Create your views here.


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
