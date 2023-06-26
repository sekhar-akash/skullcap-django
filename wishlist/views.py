from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, CreateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wishlist
from user.models import product
from django.contrib import messages
from orders.models import Order
from wishlist.models import Wallet
from django.db.models import Q
# Create your views here.

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        myproduct = get_object_or_404(product, id=product_id)
        created = Wishlist.objects.get_or_create(user=request.user, product=myproduct)
        if created:
            # Wishlist item was added successfully
            messages.success(request, 'Product added to wishlist.')
        else:
            # Wishlist item already exists
            messages.info(request, 'Product already in wishlist.')
        return redirect('wishlist:wishlist')

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        myproduct = get_object_or_404(product, id=product_id)
        Wishlist.objects.filter(user=request.user, product=myproduct).delete()
        messages.success(request, 'Product removed from wishlist.')
        return redirect('wishlist:wishlist')
    



