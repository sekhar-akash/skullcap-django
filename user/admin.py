from django.contrib import admin
from .models import product,Image

# Register your models here.
class pictureInline(admin.StackedInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','company','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('name',)}
    inlines = [pictureInline]



admin.site.register(product,ProductAdmin)