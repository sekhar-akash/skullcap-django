from django.db import models
from accounts.models import Account
from user.models import product

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Wallet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
