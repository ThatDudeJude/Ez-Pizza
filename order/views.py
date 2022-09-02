from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags import humanize
from django.http import JsonResponse
from .models import OrderedItem
from shop.models import ShoppingCartItem

# Create your views here.


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
            return render(request, 'order/ordered_list.html', {'has_delivered': len(ordered_items) > 0})    
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