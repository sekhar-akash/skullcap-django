from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payments/', views.payments,name="payments"),
    path('cash_on_delivery/', views.payment_cod, name='cash_on_delivery'),
    path('order_complete/', views.order_complete,name="order_complete"),
    path('cancel_order/<int:order_id>/',views.cancel_order, name='cancel_order'),
]
