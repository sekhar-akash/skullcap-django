from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import CreateUserForm,VerifyForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from . import verify
from .forms import UserCreationForm, VerifyForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def Register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
       
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            myuser = Account.objects.create_user(name=name,phone_number = phone_number,email=email,password = password1)
            myuser.save()
            request.session['email'] = email
            verify.send(form.cleaned_data.get('phone_number'))
            messages.success(request, 'account was successfully created')
            return redirect('verify')
        print(form.errors)
    else:
        form = CreateUserForm()
    context = {'form':form}
    return render(request,'signup.html',context)

def verify_code(request):
    email = request.session.get('email')
    if not email:
        return redirect('home')
        
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            user = Account._default_manager.get(email=email)
            if verify.check(user.phone_number, code):
                user.is_verified = True
                user.is_active = True
                user.save()
                return redirect('usersignin')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})


def SignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') 
        print('valid')

        user = authenticate(request,email=email,password=password)

        if user is not None:
            print('logged')
            login(request,user)
            if user.is_superadmin:
                request.session['email']=email
                return redirect('dashboard')
            elif user.is_blocked:
                messages.error(request,"the user is blocked")
            else:
                request.session['email']=email
                return redirect('loggedhome')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('usersignin')
        
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    request.session.flush()
    return redirect('home')
