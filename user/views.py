from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages


# Create your views here.
@login_required(login_url='/login')
@never_cache
def HomePage(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    
    return redirect('login')

@never_cache
def LoginPage(request):

    if request.method == 'POST':
        username_check = request.POST.get('username')
        password_check = request.POST.get('password')
        user = authenticate(request,username=username_check, password=password_check)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid login credentials.')
        
    return render(request,'login.html')

@never_cache
def SignupPage(request):

     
    if request.method == 'POST':
         
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password1')
        user_password_1 = request.POST.get('password2')


        #validation
        if len(user_name)<= 3 or len(user_password) <= 5:
            messages.error(request,'Password/Username is too short..!')
        elif user_password != user_password_1 or user_password == user_name or user_password == user_email:
            messages.error(request,"Password doesn't match / Password and Username should not be same...!")
        elif user_name[0].isdigit() or ' ' in user_name:
            messages.error(request,"Username Should Not Start With Numbers or ' '..! ")
        elif User.objects.filter(username = user_name).exists() or User.objects.filter(email=user_email).exists():
            messages.error(request,'User already exists...!')
        else:
            my_user = User.objects.create_user(user_name,user_email,user_password)
            my_user.save()
            return redirect('login')
            

    return render(request,'signup.html')

@never_cache
def LogoutPage(request):

    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def AdminLogin(request):
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user_admin = authenticate(request, username=username,password=password)

        if user_admin is not None and user_admin.is_superuser:
            login (request,user_admin)
            return redirect('index')
        else:

            messages.error(request,'Invalid admin credentials')

    return render(request,'adminlogin.html')

@never_cache
def AdminPage(request):

    if request.user.is_superuser:
        user_info = User.objects.all()

        context={

            'user_info': user_info
        }

        return render(request,'index.html',context)
    return redirect('login')

def AddUser(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # phone = request.POST.get('phone')

        user_data = User.objects.create_user(username,email,password)
        user_data.save()
        return redirect('index')

    
    return render(request,'index.html')

def EditUser(request):

    user_info = User.objects.all()

    context = {

        'user_info':user_info
    }

    return render(request,'index.html',context)

def UpdateUser(request,id):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data = User.objects.get(id=id)
        user_data.username = username
        user_data.email = email
        user_data.password = password
        user_data.save()
        return redirect('index')
    return render(request,'index.html')

def DeleteUserInfo(request):

    user_info = User.objects.all()
    return render(request,'index',{'userinfo':user_info})

def DeleteUser(request,id):

    user_data = User.objects.get(id=id)
    user_data.delete() 
    return redirect('index')
