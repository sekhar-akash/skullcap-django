from django.db import models
from user.models import product,Variant

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    Product =models.ForeignKey(product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variant,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.Product.price * self.quantity


    def __unicode__(self):
        return self.Product