from django import forms
from user.models import product, Image, Variant
from multiupload.fields import MultiFileField
from django.core.validators import MinValueValidator
from .models import Coupon

class ProductForm(forms.ModelForm):
    small_stock = forms.IntegerField(validators=[MinValueValidator(0)], required=False)
    medium_stock = forms.IntegerField(validators=[MinValueValidator(0)], required=False)
    large_stock = forms.IntegerField(validators=[MinValueValidator(0)], required=False)
    class Meta:
        model = product
        fields = ('name', 'slug', 'company', 'images', 'description', 'price', 'is_available', 'category')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        small_stock = self.cleaned_data.get('small_stock')
        medium_stock = self.cleaned_data.get('medium_stock')
        large_stock = self.cleaned_data.get('large_stock')
        Variant.objects.update_or_create(
            product=instance,
            variant_name='small',
            defaults={'stock': small_stock or 0}
        )
        Variant.objects.update_or_create(
            product=instance,
            variant_name='medium',
            defaults={'stock': medium_stock or 0}
        )
        Variant.objects.update_or_create(
            product=instance,
            variant_name='large',
            defaults={'stock': large_stock or 0}
        )
        return instance

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['images'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['is_available'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'

class ImageForm(forms.ModelForm):
    images = MultiFileField(max_num=5, min_num=1, required=False)

    class Meta:
        model = Image
        fields = ['images']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'min_amount', 'active', 'valid_from', 'valid_to']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'valid_from': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
            'valid_to': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'})
        }