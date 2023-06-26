from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.Home,name="home"),
    path('loggedhome/',views.LoggedHome,name="loggedhome"),
    path('dashboard/',views.dashboard,name="userdashboard"),
    path('add_address/',views.add_address,name="add-address"),
    path('delete_address/<int:address_id>/ ',views.delete_address, name="delete_address"),
    path('edit_address/<int:address_id>/',views.edit_address,name="edit_address"),
    path('activate-address/',views.activate_address,name='activate-address'),
    path('order_list/',views.order_list,name="order_list"),
    path('order/details/<int:order_id>/', views.order_details, name='order_details'),
    path('change_password/',views.change_password,name="change_password"),
]
