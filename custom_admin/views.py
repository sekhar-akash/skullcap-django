from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.shortcuts import get_object_or_404, redirect
from .models import Account
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from custom_admin.forms import ProductForm,ImageForm
from user.models import product,Image,Variant
from category.models import category
from category.forms import CategoryForm
from django.forms import inlineformset_factory
# Create your views here.
@login_required(login_url='usersignin')
def dashboard(request):
    return render(request,'custom_admin/index.html')

@login_required(login_url='usersignin')
def accounts(request):
    acc = Account.objects.all()
    return render(request,'custom_admin/accounts.html',{'accs':acc})

@login_required(login_url='usersignin')
def products(request):
    pro = product.objects.all()
    return render(request,'custom_admin/products.html',{'pro':pro})


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
            small_stock = form.cleaned_data.get('small_stock', 0)
            medium_stock = form.cleaned_data.get('medium_stock', 0)
            large_stock = form.cleaned_data.get('large_stock', 0)

            # Update or create variants based on stock values
            Variant.objects.update_or_create(
                product=product_obj,
                variant_name='small',
                defaults={'stock': small_stock or 0}
            )
            Variant.objects.update_or_create(
                product=product_obj,
                variant_name='medium',
                defaults={'stock': medium_stock or 0}
            )
            Variant.objects.update_or_create(
                product=product_obj,
                variant_name='large',
                defaults={'stock': large_stock or 0}
            )

            return redirect('products')
    else:
        form = ProductForm(instance=product_obj)
        imageform = ImageFormset(instance=product_obj, prefix='image')

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



def logoutadmin(request):
    logout(request)
    request.session.flush()
    return redirect('home')

