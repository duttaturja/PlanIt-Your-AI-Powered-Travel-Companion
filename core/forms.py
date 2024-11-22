from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'gender', 'location', 'phone_number')
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City, Country'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+1234567890'
            }),
        }
