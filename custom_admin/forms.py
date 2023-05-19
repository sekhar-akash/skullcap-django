from django import forms
from user.models import product,Image
from multiupload.fields import MultiFileField

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('name', 'slug', 'company', 'description', 'price', 'images', 'stock', 'is_available', 'category')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['images'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['is_available'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'

class images(forms.ModelForm):
    model = Image
    fields = ["product","image"]