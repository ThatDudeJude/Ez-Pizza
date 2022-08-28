

from django.shortcuts import render, redirect
from django.http import JsonResponse
# from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pasta, Platter, Salad, Sicillian, Topping, User, Regular, Sub, ShoppingCartItem, OrderedItem, SpecialSicillian, SpecialRegular
from .forms import RegisterUserForm, UpdateProfileForm

from functools import reduce
import json

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

@login_required(login_url='/user/login/')
def get_special(request, pizza):
    # print('special', pizza)
    if pizza == 'regular':
        order = SpecialRegular.objects.first()
        order_data = {"small": order.small,'large': order.large, "delicacy": order.delicacy, 'special': True}                
        response = {'data': order_data, 'toppings': None, 'name': "Regular Pizza"}
    elif pizza == 'sicillian':
        order = SpecialSicillian.objects.first()
        order_data = {"small": order.small,'large': order.large, "delicacy": order.delicacy, 'special': True}        
        response = {'data': order_data, 'toppings': None, 'name': "Sicillian Pizza"}
    
    return JsonResponse(response, safe=False)

@login_required(login_url='/user/login/')
def get_order_item(request, food_order, id):
    if food_order == 'regular':
        order = Regular.objects.get(pk=id)
        if order.delicacy == 'Special':
            order = SpecialRegular.objects.first()
            order_data = {"small": order.small,'large': order.large, "delicacy": order.delicacy, 'special': True}                
        else:
            order_data = {"small": order.small,'large': order.large, "delicacy": order.delicacy, 'special': False}                
        toppings = [{"id": topping.id, "name":topping.topping} for topping in Topping.objects.all()]        
        response = {'data': order_data, 'toppings': toppings, 'name': "Regular Pizza"}

    elif food_order == 'sicillian':
        order = Sicillian.objects.get(pk=id)
        if order.delicacy == 'Special':
            order = SpecialSicillian.objects.first()
            order_data = {"small": order.small,'large': order.large, "delicacy": order.delicacy, 'special': True}        
        else:
            order_data = {"small": order.small,'large': order.large, "delicacy": order.delicacy, 'special': False}        
        toppings = [{"id": topping.id, "name":topping.topping} for topping in Topping.objects.all()]        
        response = {'data': order_data, 'toppings': toppings, 'name': "Sicillian Pizza"}

    elif food_order == 'subs':
        order = Sub.objects.get(pk=id)
        order_data = {"small": order.small,'large': order.large, "sub": order.sub}                
        response = {'data': order_data, 'name': "Sub Sandwich"}

    elif food_order == 'pastas':
        orders = Pasta.objects.all()
        response = {'name': 'Pasta', 'data': []}
        for order in orders:            
            response['data'].append({'delicacy' : order.pasta, 
            'fixed' : order.fixed})

    elif food_order == 'salads':
        orders = Salad.objects.all()
        response = {'name': 'Salad', 'data': []}
        for order in orders:
            response['data'].append({'delicacy': order.salad, 
            'fixed': order.fixed})

    elif food_order == 'platters':
        order = Platter.objects.get(pk=id)
        order_data = {"small": order.small,'large': order.large, "platter": order.platter}                
        response = {'data': order_data, 'name': "Dinner Platter"}

    return JsonResponse(response, safe=False)

@login_required(login_url='/user/login/')
def shop_pizza(request):

    if request.method == 'POST':
        # print("request", request.body)
        form_data = json.load(request)
        # print(form_data)
        food =  form_data['item'] 
        size = f"{' + '.join([f'{key}' for key in form_data.keys() if key == 'small' or key =='large'])}"        
        price = "%.2f"%reduce(lambda a, b: a + b, [float(form_data[key]) for key in form_data.keys() if key == 'small' or key =='large'])
        if form_data.get('type'):
            info = f"{form_data.get('special', '')}{form_data['type']}"
        else:
            info = f"Topping(s): {', '.join([f'{form_data[key]}' for key in form_data.keys() if key.startswith('topping')])}"
        # print(f"pizza: {food + info} price: {price}")
        response = {"food": food + f" ({size})",  "info": info, 'price': price}
        # print(f"size {form_data}")

        return JsonResponse({"error": False, "message": response})

    return JsonResponse({"error": True, "message": "Something went wrong!"})

@login_required(login_url='/user/login/')
def shop_sub(request):

    if request.method == 'POST':
        form_data = json.load(request)
        # print(f"sub order: {form_data}")        
        food = form_data['item']
        size = f"{' + '.join([f'{key}' for key in form_data.keys() if key == 'small' or key =='large'])}"        
        price = "%.2f"%reduce(lambda a, b: a + b, [float(form_data[key]) for key in form_data.keys() if key == 'small' or key =='large' or key.startswith('+')])
        info = f"{form_data['type']} " + " ".join([
            f'{extra}'for extra in form_data.keys() if extra.startswith('+')
        ])
        # print({"food": food + f" ({size})",  "info": info, 'price': price})
        response = {"food": food + f" ({size})",  "info": info, 'price': price}        
        return JsonResponse({"error": False, "message": response})

    return redirect('index')

@login_required(login_url='/user/login/')
def shop_pasta(request):

    if request.method == 'POST':
        form_data = json.load(request)        
        # print(f"pasta order: {form_data}")
        food = form_data['item']
        price = "%.2f"%reduce(lambda a, b: a + b, [float(form_data[key]) for key in form_data.keys() if key.startswith('Baked')])
        info = ", ".join([f'{key}' for key in form_data.keys() if key.startswith('Baked')])
        # print({"food": food,  "info": info, 'price': price})
        response = {"food": food,  "info": info, 'price': price}        
        return JsonResponse({"error": False, "message": response})

    return redirect('index')

@login_required(login_url='/user/login/')
def shop_salad(request):

    if request.method == 'POST':
        form_data = json.load(request)                
        # print(f"salad order: {form_data}")
        food = form_data['item']
        price = "%.2f"%reduce(lambda a, b: a + b, [float(form_data[key]) for key in form_data.keys() if key.startswith('salad')])
        info = ", ".join([f'{key.split("-")[1]}' for key in form_data.keys() if key.startswith('salad-')])
        # print({"food": food,  "info": info, 'price': price})
        response = {"food": food,  "info": info, 'price': price}        
        return JsonResponse({"error": False, "message": response})

    return redirect('index')

@login_required(login_url='/user/login/')
def shop_platter(request):

    if request.method == 'POST':
        form_data = json.load(request)
        # print(f"sub order: {form_data}")        
        food = form_data['item']
        size = f"{' + '.join([f'{key}' for key in form_data.keys() if key == 'small' or key =='large'])}"        
        price = "%.2f"%reduce(lambda a, b: a + b, [float(form_data[key]) for key in form_data.keys() if key == 'small' or key =='large'])
        info = f"{form_data['type']}"
        # print({"food": food + f" ({size})",  "info": info, 'price': price})
        response = {"food": food + f" ({size})",  "info": info, 'price': price}        
        return JsonResponse({"error": False, "message": response})

    return redirect('index')

@login_required(login_url='/user/login/')
def shopping_cart(request):
    shopping_items = ShoppingCartItem.objects.filter(client=request.user).count()
    return JsonResponse({"items": shopping_items})

@login_required(login_url='/user/login/')
def add_order_item(request):

    if request.method == 'POST':
        order_data = json.load(request)
        new_order = ShoppingCartItem(client=request.user, food_item=order_data['food'], choices=order_data['info'], price=order_data['price'])
        new_order.save()
        # print("add order", order_data)

    return redirect('index')

@login_required(login_url='/user/login/')
def get_shopping_cart_data(request):
    shopping_cart = ShoppingCartItem.objects.filter(client=request.user)
    total_price = 0
    shopping_cart_items = []
    for item in shopping_cart.values(): 
        # print('item', item)        
        total_price += float(item['price'])
        shopping_cart_items.append(item)
    context = {'shopping_cart': shopping_cart_items, 'total_price': '%.2f'% total_price}
    return context

@login_required(login_url='/user/login/')
def show_shopping_cart(request, access='denied'):    
    print('access', access)
    if request.user.is_authenticated:        
        context = get_shopping_cart_data(request)
        if access == 'page':
            return render(request, 'base/shopping_list.html', context)
        elif access == 'data':                      
            return JsonResponse(context)
        

@login_required(login_url='/user/login/')
def delete_shopping_item(request, id):
    
    if request.user.is_authenticated and request.method == 'DELETE':        
        try:
            shopping_cart_item = ShoppingCartItem.objects.get(pk=id)
            shopping_cart_item.delete()

            return JsonResponse({'error': False, 'message': 'Deleted from Cart'}) 
        except:

            return JsonResponse({'error': True, 'message': 'Something went wrong'})

    shopping_cart_item = ShoppingCartItem.objects.get(pk=id)
    data = {'action': 'delete', 'food_item': shopping_cart_item.food_item, 'choices': shopping_cart_item.choices, 'price': shopping_cart_item.price}
    return JsonResponse(data)

@login_required(login_url='/user/login/')
def order_shopping_items(request):
    print('ordering')
    if request.user.is_authenticated and request.method == 'POST':        
        try:
            print('ordering from cart')
            shopping_cart = ShoppingCartItem.objects.filter(client=request.user)
            for item in shopping_cart:                 
                order_item = OrderedItem(client=request.user, 
                food_item=item.food_item, 
                choices=item.choices, 
                price=item.price)

                order_item.save()
                item.delete()

            return JsonResponse({'error': False, 'message': 'Order Completed'}) 
        except:
            print('ordering from cart went wrong')
            return JsonResponse({'error': True, 'message': 'Something went wrong'})
    return redirect('show_ordered_items', status= 'ALL')

def get_time(created):
    return humanize.naturaltime(created)

@login_required(login_url='/user/login/')
def show_ordered_items(request, status):
    
    if request.user.is_authenticated:        
        if status == 'retrieve':
            ordered_items = OrderedItem.objects.filter(status='DELIVERED')            
            return render(request, 'base/ordered_list.html', {'has_delivered': len(ordered_items) > 0})    
        elif status.lower() != 'all':
            ordered_items = OrderedItem.objects.filter(client=request.user).filter(status=f'{status.upper()}').order_by('-created')        
        else: 
            ordered_items = OrderedItem.objects.filter(client=request.user).order_by('-created')
        items = []
        for item in ordered_items.values(): 
            # item['created'] = item.get_time
            item['human_time'] = get_time(item['created'])
            items.append(item)
        return JsonResponse(items, safe=False)
    return redirect('index')

@login_required(login_url='/user/login/')
def delete_delivered_orders(request):
    if request.user.is_authenticated:
        OrderedItem.objects.filter(client=request.user).filter(status='DELIVERED').delete()

    return redirect('show-ordered-items', status='retrieve')