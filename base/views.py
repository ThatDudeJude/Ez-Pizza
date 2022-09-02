from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from .models import User
from shop.models import Pasta, Platter, Salad, Sicillian, Topping, Regular, Sub, ShoppingCartItem,  SpecialSicillian, SpecialRegular
from django.contrib.auth import login, logout, authenticate

from django.contrib import messages

from .forms import RegisterUserForm, UpdateProfileForm


# Create your views here.

def login_user(request):    
    if request.user.is_authenticated:
        return redirect('index')
    
    auth = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)            
        except: 
            messages.error(request, 'email does not exist.')
            
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Wrong password.')                        
        
    context = {"auth": auth}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')

def register_user(request):
    auth = 'register'    
    form = RegisterUserForm()
    context = {'auth': auth, 'form': form}
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        print('submitting')
        if form.is_valid():
            user = form.save()            
            login(request, user)
            
            return redirect('index')
        else:            
            context = {'auth': auth, 'form': form}            
    
    
    return render(request, 'base/login_register.html', context)

@login_required(login_url='/user/login')
def get_user_profile(request, action):
    if action == 'view':
        context = {'profile': request.user, 'type': 'view'}
        return render(request, 'base/profile.html', context)
    else:
        form = UpdateProfileForm(instance=request.user)
        
        context = {'form': form, 'type': 'update'}

        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            context = {'profile': request.user, 'type': 'view'}
            return render(request, 'base/profile.html', context)

        return render(request, 'base/profile.html', context)


def index(request):
    
    regular_pizzas = Regular.objects.all()
    sicillian_pizzas = Sicillian.objects.all()
    toppings = Topping.objects.all()
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    platters = Platter.objects.all()
    special_regular = SpecialRegular.objects.first()
    special_sicillian = SpecialSicillian.objects.first()    
    
    context = {
        'user': request.user, 
        'regular_pizzas': regular_pizzas, 
        'sicillian_pizzas': sicillian_pizzas, 
        'toppings': toppings,
        'subs': subs, 
        'pastas': pastas,
        'salads': salads,
        'platters': platters, 
        'special_regular' : special_regular,
        'special_sicillian' : special_sicillian,
    }        
    
    return render(request, 'base/index.html', context)
