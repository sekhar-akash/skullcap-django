from django.shortcuts import render,redirect,get_list_or_404
from orders.forms import OrderForm
from user.models import product,Variant
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import Address
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from custom_admin.models import Coupon
from datetime import date
import json
from django.utils import timezone
from decimal import Decimal
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    products = product.objects.get(id = product_id)
    if current_user.is_authenticated:
        product_variation =[]
        if request.method == 'POST':
            for item in request.POST:
                if item!='csrfmiddlewaretoken':
                    key = item 
                    value = request.POST[key]
                    variation = Variant.objects.get(product=products, variant_name=value)
                    product_variation.append(variation)
        
        

        is_cart_item_exists = CartItem.objects.filter(Product=products,user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(Product=products, user = current_user)

            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(Product=products, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(Product=products, quantity =1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(product_variation[0])
                item.save()
        else:
            cart_item = CartItem.objects.create(Product=products,quantity = 1, user=current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(product_variation[0])
            cart_item.save()
        return redirect('cart')
#if the user is not authenticated
    else:
        product_variation =[]
        if request.method == 'POST':
            for item in request.POST:
                if item!='csrfmiddlewaretoken':
                    key = item 
                    value = request.POST[key]
                    variation = Variant.objects.get(product=products, variant_name=value)
                    product_variation.append(variation)
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(Product=products,cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(Product=products, cart = cart)

            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(Product=products, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(Product=products, quantity =1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(product_variation[0])
                item.save()
        else:
            cart_item = CartItem.objects.create(Product=products,quantity = 1, cart= cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(product_variation[0])
            cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id,cart_item_id):
    products =  product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item =CartItem.objects.get(Product=products, user = request.user ,id = cart_item_id)
        else:
            cart_item = CartItem.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(Product=products, cart=cart,id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id,cart_item_id):
    
    products = product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item =CartItem.objects.get(Product=products, user = request.user ,id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(Product=products, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    
    try:
        shipping = 40
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            # cart_items = cart.cartitem_set.all()

        for cart_item in cart_items:
            total += (cart_item.Product.price * cart_item.quantity)
            quantity += cart_item.quantity
        shipping = 40
        grand_total = shipping + total

        if(request.session.get('total')):
            grand_total=request.session.get('total')
            print(grand_total,"***************************")

    except ObjectDoesNotExist:
        pass
    
    context ={
        'total' :total,
        'quantity' :quantity,
        'cart_items' : cart_items,
        'shipping' : shipping,
        'grand_total' : grand_total,
    }
    return render(request,'shopping-cart.html',context)


@login_required(login_url='usersignin')
def checkout(request, total=0, quantity=0, cart_items=None):

    shipping = 40
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.Product.price * cart_item.quantity)
            quantity += cart_item.quantity
        shipping = 40
        grand_total = shipping + total

        
        
    except ObjectDoesNotExist:
        pass

    form = OrderForm()
    saved_addresses = Address.objects.filter(user=request.user).order_by('-id')
    cadd = Address.objects.filter(user=request.user, status=True).first()

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping': shipping,
        'grand_total': grand_total,
        'form': form,
        'saved_addresses': saved_addresses,
        'cadd': cadd
    }
    return render(request, 'check-out.html', context)





@require_POST
def apply_coupon(request):
    body = json.loads(request.body)
    grand_total = int(body['grand_total'])
    coupon_code = body['coupon']
    try:
        coupon = Coupon.objects.get(code__iexact=coupon_code)
    except Coupon.DoesNotExist:
        data = {
            "total": grand_total,
            "message": "Not a Valid Coupon"
        }
    else:
        today = date.today()
        valid_from = coupon.valid_from.date()
        valid_to = coupon.valid_to.date()
        min_amount = int(coupon.min_amount)
        if min_amount < grand_total and valid_from <= today <= valid_to:
            grand_total = grand_total - int(coupon.discount)
            request.session['total'] = grand_total  # Update the session variable
            data = {
                "total": grand_total,
                "message": f"{coupon.code} Applied"
            }
        else:
            data = {
                "total": grand_total,
                "message": "Not a Valid Coupon"
            }
    return JsonResponse(data)
