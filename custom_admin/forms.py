from django import forms
from user.models import product, Image, Variant
from multiupload.fields import MultiFileField

class ProductForm(forms.ModelForm):
    small_stock = forms.IntegerField(label='Small Stock', required=False)
    medium_stock = forms.IntegerField(label='Medium Stock', required=False)
    large_stock = forms.IntegerField(label='Large Stock', required=False)
    

    class Meta:
        model = product
        fields = ('name', 'slug', 'company','images', 'description', 'price', 'is_available', 'category')
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
        if small_stock is not None:
            variant_small = Variant(product=instance, variant_name='Small', stock=small_stock)
            variant_small.save()
        if medium_stock is not None:
            variant_medium = Variant(product=instance, variant_name='Medium', stock=medium_stock)
            variant_medium.save()
        if large_stock is not None:
            variant_large = Variant(product=instance, variant_name='Large', stock=large_stock)
            variant_large.save()
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