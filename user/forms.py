from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','pin_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Post Code/ZIP'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }