from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

class CreateUserForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'label': 'name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','label':'phone_number',}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'label': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'label': 'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'label': 'password2'}))

    class Meta:
        model = Account
        fields = ['name','phone_number','email','password1','password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')
