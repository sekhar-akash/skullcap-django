
from django.db import models
from category.models import category
from django.utils import timezone
from django.urls import reverse
from accounts.models import Account
from django.core.validators import MinValueValidator

# Create your models here.

class product(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    company = models.CharField(max_length=200,blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    images = models.ImageField(upload_to='photos/products', null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name
    


class Variant(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=200)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.variant_name
    
class Image(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='photos/products', null=True)

    def __str__(self):
        return self.image.url

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=20,null=True)
    status = models.BooleanField(default=False)


    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    
