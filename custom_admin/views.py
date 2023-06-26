import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime,timedelta, timezone
from orders.models import OrderProduct
from .models import Account
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate,login,logout
from custom_admin.forms import ProductForm,ImageForm,CouponForm
from user.models import product,Image,Variant
from category.models import category
from category.forms import CategoryForm
from django.forms import inlineformset_factory
from orders.models import Order
from . models import Coupon
from  django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
@login_required(login_url='usersignin')
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:5]
    users = Account.objects.all()
    users_count = users.count()

    myproducts = product.objects.all().order_by('-id')

    categories = category.objects.all()
    category_count = categories.count()

    total_order = Order.objects.all()
    total_orders = total_order.count()

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    dates = [start_of_week + timedelta(days=i) for i in range(7)]
    sales = []
    for date in dates:
        Orders = OrderProduct.objects.filter(
            ordered=True,
            created_at__year=date.year,
            created_at__month=date.month,
            created_at__day=date.day,
        )
        total_sales = sum(order.product_price * order.quantity for order in Orders)
        sales.append(total_sales)
    sums = sum(sales)
    product_count = myproducts.exclude(orderproduct__ordered=True).count()
    context = {
        'orders': orders,
        'product_count': product_count,
        'category_count': category_count,
        'products': myproducts,
        'total_orders': total_orders,
        "users_count": users_count,
        'dates': dates,
        'sales': sales,
        'sums': sums,
    }
    return render(request,'custom_admin/index.html', context)

def add_order_filter(request):
    body = json.loads(request.body)
    try:
        start_date =datetime.strptime(body['from'],'%Y-%m-%d')
        end_date = datetime.strptime(body['to'],'%Y-%m-%d')
    except ValueError:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=end_date.weekday())
    try:
        orders = Order.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
        json_data = serializers.serialize('json', orders)
    except Order.DoesNotExist:
        orders = None     
    data ={
             "order":json_data,
            }
    return JsonResponse(data)

@login_required(login_url='usersignin')
def accounts(request):
    acc = Account.objects.all()
    return render(request,'custom_admin/accounts.html',{'accs':acc})

@login_required(login_url='usersignin')
def products(request):
    pro =product.objects.prefetch_related('variants')
    return render(request,'custom_admin/products.html',{'pro':pro})

def orders(request):
    ord = Order.objects.all().order_by('-id')
    return render(request,'custom_admin/orders.html',{'ord':ord})

def order_details_admin(request,order_id):
    subtotal=0
    shipping = 40
    order = Order.objects.get(id=order_id)
    order_product = OrderProduct.objects.filter(order_id = order)
    for i in order_product:
        subtotal += i.product_price * i.quantity
    context = {
        'order_product': order_product,
        'order': order,
        'subtotal': subtotal,
        'shipping': shipping,
        'order_number': order.order_number,
    }
    
    return render(request,'custom_admin/order_details_admin.html',context)

def change_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass
    return redirect('orders')


def block_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    if user.is_superadmin == True:
        return HttpResponse('cant block admin')
    else:
        user.is_blocked = True
        user.save()
        return redirect('accounts')

def unblock_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('accounts')

productImageFormset = inlineformset_factory(product, Image,form=ImageForm, extra=3)
from django.forms.models import inlineformset_factory

ImageFormset = inlineformset_factory(product, Image, form=ImageForm, extra=3)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        imageform = ImageFormset(request.POST, request.FILES)

        if form.is_valid() and imageform.is_valid():
            new_product = form.save()

            
            for image_form in imageform:
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.product = new_product
                    image.save()


            # Save variant stock
            small_stock = form.cleaned_data['small_stock']
            medium_stock = form.cleaned_data['medium_stock']
            large_stock = form.cleaned_data['large_stock']

            # Update or create variants based on stock values
            Variant.objects.update_or_create(product=new_product, variant_name='small', defaults={'stock': small_stock})
            Variant.objects.update_or_create(product=new_product, variant_name='medium', defaults={'stock': medium_stock})
            Variant.objects.update_or_create(product=new_product, variant_name='large', defaults={'stock': large_stock})

            return redirect('products')
        else:
            print('Form errors:', form.errors, imageform.errors)
    else:
        form = ProductForm()
        imageform = ImageFormset()

    categories = category.objects.all()
    context = {
        'form': form, 
        'categories': categories,
        'imageform': imageform
        }
    return render(request, 'custom_admin/add-product.html',context)




def edit_product(request, id):
    product_obj = get_object_or_404(product, id=id)

    # Exclude duplicate variants from the queryset
    product_variants = Variant.objects.filter(product=product_obj).distinct()

    ImageFormset = inlineformset_factory(product, Image, form=ImageForm, extra=0)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_obj)
        imageform = ImageFormset(request.POST, request.FILES, instance=product_obj)
        if form.is_valid() and imageform.is_valid():
            form.save()
            imageform.save()

            # Save variant stock
            small_stock = form.cleaned_data.get('small_stock')
            medium_stock = form.cleaned_data.get('medium_stock')
            large_stock = form.cleaned_data.get('large_stock')

            # Update or create variants based on stock values
            Variant.objects.filter(product=product_obj, variant_name='small').update(stock=small_stock or 0)
            Variant.objects.filter(product=product_obj, variant_name='medium').update(stock=medium_stock or 0)
            Variant.objects.filter(product=product_obj, variant_name='large').update(stock=large_stock or 0)

            return redirect('products')
    else:
        form = ProductForm(instance=product_obj)
        imageform = ImageFormset(instance=product_obj, queryset=Image.objects.filter(product=product_obj))

    context = {
        'form': form,
        'product': product_obj,
        'imageform': imageform,
        'product_variants': product_variants,
    }
    return render(request, 'custom_admin/edit-product.html', context)



def delete_product(request, product_id):
    products = product.objects.get(id=product_id)
    products.delete()
    return redirect('products')

##############################################################################################################################################

@login_required(login_url='usersignin')
def categories(request):
    cat = category.objects.all()
    return render(request,'custom_admin/category.html', {'cat' : cat})

def delete_category(request, category_id):
    category_obj = get_object_or_404(category, id=category_id)
    
    if request.method == 'POST':
        category_obj.delete()
        return redirect('category') 
    return render(request, 'custom_admin/delete-category.html', {'category': category_obj})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    
    return render(request, 'custom_admin/add-category.html', {'form': form})

#####################################################################################################################################################

def coupen_manage(request):
    coupons = Coupon.objects.all()

    context = {
        'coupons' : coupons
    }

    return render(request, 'custom_admin/coupon_manage.html', context)

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_managee')
    else:
        form = CouponForm()

    context = {'form': form}
    return render(request, 'custom_admin/add_coupon.html', context)

def delete_coupons(request,id):
    if request.method == "POST":
        try:

            coup = Coupon.objects.get(id=id)
            coup.delete()
        except ObjectDoesNotExist:
            pass

    return redirect('coupon_manage')

def edit_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        form = CouponForm(request.POST, instance=coup)
        if form.is_valid:
            form.save()
        return redirect('coupon_manage')
    else:
        coup = Coupon.objects.get(id=id)
        form = CouponForm(instance=coup)
        context = {
            "form" : form
        }
    return render(request, 'custom_admin/edit_coupon.html', context)




def logoutadmin(request):
    logout(request)
    request.session.flush()
    return redirect('home')

