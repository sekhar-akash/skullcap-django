from django.shortcuts import render
from user.models import product
from django.contrib.auth.decorators import login_required
from accounts.decorators import verification_required
from category.models import category
# Create your views here.

def Home(request):
    products = product.objects.all().filter(is_available=True)
    context = {
        'products' : products,
    }
    return render(request,'index.html',context)



# @login_required(login_url='usersignin')
# @verification_required
def LoggedHome(request):
    products = product.objects.all().filter(is_available=True)
    context = {
        'products' : products
    }
    return render(request,'index1.html',context)