from django.shortcuts import render,redirect
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order,Payment,OrderProduct
import json
from user.models import product
# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

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

    return render(request,'orders/payments.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user


    #if the cart count is less than or equal to 0, then redirect to storepage
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0 :
        return redirect('storepage')
    
    grand_total=0
    shipping = 40
    for cart_item in cart_items:
        total += (cart_item.Product.price * cart_item.quantity)
        quantity += cart_item.quantity
    shipping = 40
    grand_total = shipping + total
    
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            print("inside form valid")
            # store all billing information inside oreder table
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

            #generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user,is_ordered = False, order_number=order_number)
            context = {
                'order' :order,
                'cart_items':cart_items,
                'total':total,
                'shipping':shipping,
                'grand_total':grand_total
            }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')
         