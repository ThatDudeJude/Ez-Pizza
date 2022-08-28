from ast import Pass
from cProfile import label
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, PasswordInput, CharField, ImageField, FileInput
from django.forms import ModelForm
from .models import User


class RegisterUserForm(UserCreationForm):
    password1 = CharField(
        label="Password", 
        widget=PasswordInput(attrs={'class': 'form-control', 'type': 'password',
        'placeholder': 'password'})
    )
    password2 = CharField(
        label="Confirm Password", 
        widget=PasswordInput(attrs={'class': 'form-control', 'type': 'password',
        'placeholder': 'Confirm password'})
    )
    class Meta:
        model = User 
        fields = ['name', 'username', 'email']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',                
            }),
            'username': TextInput(attrs={
                'class': 'form-control',                
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',                
            }),
            # 'password1': PasswordInput(attrs={
            #     'class': 'form-control',                
            # })

        }


class UpdateProfileForm(ModelForm):
    # avatar = ImageField(label='Avatar', 
    #         widget=)        
    class Meta:
        model = User 
        fields = ['avatar', 'name', 'username', 'email']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',                
            }),
            'username': TextInput(attrs={
                'class': 'form-control',                
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',                            
            }),
            'avatar': FileInput(attrs={
                'class': 'form-control',
            })
        }
