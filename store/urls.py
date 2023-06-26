from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.storePage,name="storepage"),
    path('category/<slug:category_slug>/',views.storePage, name="products_category"),
    path('category/<slug:category_slug>/<slug:product_slug>',views.productDetail, name="product_detail"),
    path('search/',views.search, name='search'),
    path('products/', views.product_filter, name='product_filter')
]
