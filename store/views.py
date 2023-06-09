from django.shortcuts import render,get_object_or_404
from user.models import product,Variant,Image
from category.models import category
from carts.models import CartItem
from django.http import HttpResponse
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q


# Create your views here.

def storePage(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(category,slug=category_slug)
        products = product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request, 'store/categories.html', context)



def productDetail(request, category_slug, product_slug):
    try:
        single_product = product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), Product=single_product).exists()
        product_variants=Variant.objects.filter(product=single_product)
        product_images = Image.objects.filter(product=single_product)
        print(product_images)
    except Exception as e:
        raise e
    
    context ={
        'single_product' : single_product,
        'in_cart' : in_cart,
        'product_variant':product_variants,
        'product_images': product_images,
    }
    return render(request,'store/product-page.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    products = product.objects.none()  # Initialize products with an empty queryset
    product_count = 0

    if keyword:
        products = product.objects.order_by('-created_date').filter(
            Q(description__icontains=keyword) | Q(name__icontains=keyword)
        )
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/categories.html', context)



def product_filter(request):
    companies = product.objects.values('company').distinct()
    selected_company = request.GET.get('company')  # Get the selected company from the query parameters
    filtered_products = product.objects.filter(company=selected_company) if selected_company else product.objects.all()

    context = {
        'companies': companies,
        'selected_company': selected_company,
        'products': filtered_products
    }
    return render(request, 'store/categories.html', context)
