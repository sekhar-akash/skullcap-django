from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import CreateUserForm,VerifyForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from . import verify
from .forms import UserCreationForm, VerifyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carts.models import Cart,CartItem
from carts.views import _cart_id
import requests

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
            return redirect('verify')
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

        user = authenticate(request,email=email,password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list =[]
                    id =[]
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pro in product_variation:
                        if pro in ex_var_list:
                            index = ex_var_list.index(pro)
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                item.user = user
                                item.save()       
            except:
                pass
            
            login(request,user)
            if user.is_superadmin:
                request.session['email']=email
                return redirect('dashboard')
            elif user.is_blocked:
                messages.error(request,"the user is blocked")
            else:
                request.session['email']=email
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('loggedhome')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('usersignin')
        
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    request.session.flush()
    return redirect('home')



    

