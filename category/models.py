from django.db import models
from django.urls import reverse
# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150,unique=True)
    description = models.TextField(max_length=400, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
            return reverse('products_category', args=[self.slug])

    def __str__(self):
        return self.name
