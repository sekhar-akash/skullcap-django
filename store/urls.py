from django.urls import path,include
from . import views
urlpatterns = [
    path('storepage/',views.storePage,name="storepage"),
    path('storepage/<slug:category_slug>/',views.storePage, name="products_category"),
    path('storepage/<slug:category_slug>/<slug:product_slug>',views.productDetail, name="product_detail"),
]
