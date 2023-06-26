import random
from django.shortcuts import get_object_or_404, render,redirect
from carts.models import CartItem

from .forms import OrderForm, ReturnForm
import datetime
from .models import Order,Payment,OrderProduct, Return
import json
from user.models import product as Product
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from user.models import Address
from wishlist.models import Wallet
# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status']
    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()

    #move the cart items to order product table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = order.user.id
        orderproduct.product_id = item.Product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.Product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()



        #reduce the quantity of sold products
        product_obj = item.Product
        variant_obj = item.variations.first() 
        if variant_obj:
            variant_obj.stock -= item.quantity
            variant_obj.save()
        else:
            product_obj.stock -= item.quantity
            product_obj.save()

        # item.delete()
    CartItem.objects.filter(user=request.user).delete()


    #send order number and transaction id back to sendData method via jsonResonce

    data = {
        'order_number' : order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

def payment_cod(request):
    # body = json.loads(request.body)
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%Y%m%d")

    random_number = random.randint(1, 1000)
    
    # Combine current date and random number to create the order number
    order_num = current_date + str(random_number)
    print(order_num)
    order = Order.objects.latest('created_at')
    # order = Order.objects.get(user = request.user, is_ordered = False)

    payment = Payment(
        user=request.user,
        payment_method="COD",
        amount_paid=order.order_total,
        status= "New"
    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()

    #move the cart items to order product table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = order.user.id
        orderproduct.product_id = item.Product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.Product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()



        #reduce the quantity of sold products
        product_obj = item.Product
        variant_obj = item.variations.first() 
        if variant_obj:
            variant_obj.stock -= item.quantity
            variant_obj.save()
        else:
            product_obj.stock -= item.quantity
            product_obj.save()

        # item.delete()
    CartItem.objects.filter(user=request.user).delete()

    context = {
        'order' : order,
        'order_number' : order_num,

    }
    return render(request,'orders/order_complete.html',context)





def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, redirect to storepage
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('storepage')

    grand_total = 0
    shipping = 40
    for cart_item in cart_items:
        total += (cart_item.Product.price * cart_item.quantity)
        quantity += cart_item.quantity
    grand_total = shipping + total
    if(request.session.get('total')):
            grand_total=request.session.get('total')

    saved_addresses = Address.objects.filter(user=current_user)
    

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():

            # Create a new order instance
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin_code = form.cleaned_data['pin_code']

            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'shipping': shipping,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        form = OrderForm()
        form.fields['selected_address'].choices = [(address.id, str(address)) for address in saved_addresses]
        context = {
            'saved_addresses': saved_addresses,
            'form': form,
            'cart_items': cart_items,
            'total': total,
            'shipping': shipping,
            'grand_total': grand_total,
        }
        return render(request, 'check-out.html', context)

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)

        subtotal = 0
        shipping = 40
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal' : subtotal,
            'shipping' : shipping,
        }
        return render(request,'orders/order_complete.html',context)
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('loggedhome')
    
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'cancelled':
        pass
    else:
        for order_product in order.orderproduct_set.all():
            product = order_product.product
            variant = product.variants.first() 
            variant.stock += order_product.quantity
            variant.save()
        order.status = 'cancelled'
        order.save()

        wallet, created = Wallet.objects.get_or_create(user=order.user)
        wallet.balance += order.order_total
        wallet.save()
    return redirect('order_list')

def return_order(request,order_id, product_id):
    order = Order.objects.get(id = order_id)
    if order.customer != request.user:
        return redirect("home")

    
    if request.method == "POST":
        form = ReturnForm(request.POST)
        if form.is_valid():
            product_id = product_id
            product = Product.objects.all(id = product_id)
            orderItem = OrderProduct.objects.get(order = order, product  = product)
            reason = form.cleaned_data["reason"]
            new_return = Return(
                order=order,
                product=orderItem,
                reason=reason,
                status="pending",
                user=request.user
            )
            new_return.save()
            order.status = "Return Requested"
            orderItem.status = "Return Requested"
            orderItem.save()
            order.save()
            return redirect(order_details, id=order_id)
    else:
        form = ReturnForm()
        product = Product.objects.get(id=product_id)
        orderItem = OrderProduct.objects.get(order = order, product = product)
        form.product = orderItem
        print(orderItem.product)
    return render(request, "cart/return_product.html", {"order": order, "form": form, 'order_item':orderItem})
         