from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('accounts/',views.accounts,name="accounts"),
    path('products/',views.products, name="products"),
    path('addproduct/',views.add_product,name="addProduct"),
    path('product/<int:id>/edit/', views.edit_product, name='editproduct'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('block/<int:user_id>/',views.block_user, name='block_user'),
    path('unblock/<int:user_id>/',views.unblock_user, name='unblock_user'),
    path('category/',views.categories,name="category"),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('customadmin/category/add/',views.add_category, name='addcat'),
    path('logoutadmin',views.logoutadmin,name="logoutadmin")
]
