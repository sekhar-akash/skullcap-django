from django.contrib import admin
from .models import product,Image,Variant

# Register your models here.
class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0
class pictureInline(admin.StackedInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'get_variant_stock', 'price', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VariantInline, pictureInline]

    def get_variant_stock(self, obj):
        return ', '.join([f'{variant.variant_name}: {variant.stock}' for variant in obj.variants.all()])
    get_variant_stock.short_description = 'Variant Stock'

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variant_name', 'stock', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variant_name', 'stock')

admin.site.register(product,ProductAdmin)
admin.site.register(Variant,VariationAdmin)
