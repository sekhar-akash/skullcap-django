from django.urls import path
from .views import WishlistListView, AddToWishlistView, RemoveFromWishlistView
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', WishlistListView.as_view(), name="wishlist"),
    path('wishlist/add/<int:product_id>/', AddToWishlistView.as_view(), name="add_to_wishlist"),
    path('wishlist/remove/<int:product_id>/', RemoveFromWishlistView.as_view(), name="remove_from_wishlist"),
    
]
