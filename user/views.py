from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from user.models import product,Address
from django.contrib.auth.decorators import login_required
from accounts.decorators import verification_required
from category.models import category
from .forms import AddressForm
from django.contrib import messages
from orders.models import Order,OrderProduct,Payment
from django.core.exceptions import ObjectDoesNotExist
from wishlist.models import Wallet
from accounts.models import Account

# Create your views here.

def Home(request):
    products = product.objects.all().filter(is_available=True)
    context = {
        'products' : products,
    }
    return render(request,'index.html',context)



@login_required(login_url='usersignin')
@verification_required
def LoggedHome(request):
    products = product.objects.all().filter(is_available=True)
    context = {
        'products' : products
    }
    return render(request,'index1.html',context)

@login_required(login_url='usersignin')
def dashboard(request):
    current_user = request.user

    acc = Address.objects.filter(user = request.user)
    
    order_count = Order.objects.filter(user=current_user).count()

    wallet = Wallet.objects.get(user = request.user)
    

    context = {
        'acc' : acc,
        'order_count' : order_count,
        'wallet' : wallet,
    }
    return render(request, 'user_dashboard/dashboard.html',context)

def order_list(request):
    ord = Order.objects.filter(user=request.user, is_ordered = True).order_by('-created_at')
    
    return render(request, 'user_dashboard/order_list.html',{'ord' : ord})

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order_id = order.id)
    
    print(order, ordered_products)
    subtotal = 0
    shipping = 40
    for i in ordered_products:
        subtotal += i.product_price * i.quantity
    context = {
        'order':order,
        'ordered_products':ordered_products,
        'order_number':order.order_number,
        'subtotal' : subtotal,
        'shipping' : shipping,
        }

    return render(request, 'user_dashboard/order_details.html',context)

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            print(request.user.name) 
            address.save()
            messages.success(request, 'Address saved successfully')
            return redirect('userdashboard')
    else:
        form = AddressForm()

    saved_addresses = Address.objects.filter(user=request.user) 

    context = {
        'form': form,
        'saved_addresses': saved_addresses,
    }
    return render(request, 'user_dashboard/add_address.html', context)


def activate_address(request):
    a_id = request.GET['id']
    Address.objects.update(status= False)
    Address.objects.filter(id=a_id).update(status=True)
  
    return JsonResponse({'bool':True})



def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully')
            return redirect('userdashboard')
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
        'address_id': address_id
    }
    return render(request, 'user_dashboard/edit_address.html', context)

def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    return redirect('userdashboard')

@login_required 
def change_password(request):
    if request.method == 'POST':
        currentpassword = request.POST['current_password']
        newpassword = request.POST['new_password']
        conformpassword = request.POST['conform_password']

        myuser = Account.objects.get(email__exact=request.user.email)

        if newpassword == conformpassword:
            success = myuser.check_password(currentpassword)
            if success:
                myuser.set_password(newpassword)
                myuser.save()
                messages.success(request,'password updated sucessfully')
                return redirect('change_password')
            else:
                messages.error(request,'Current Password is invalid!!!')
                return redirect('change_password')
        else:
            messages.error(request,"Password Does't Match")
            return redirect('change_password')
    return render(request,'user_dashboard/change_password.html')

