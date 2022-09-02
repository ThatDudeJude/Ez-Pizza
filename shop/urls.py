from django.urls import path 
from . import views 


urlpatterns  = [     
    path('shopping/<str:food_order>/<str:id>/', views.get_order_item, name="food-order"),
    path('add/special/<str:pizza>/', views.get_special, name='shop-special'),
    path('add/pizza/', views.shop_pizza, name='shop-pizza'),
    path('add/sub/', views.shop_sub, name='shop-sub'),
    path('add/pasta/', views.shop_pasta, name='shop-pasta'),
    path('add/salad/', views.shop_salad, name='shop-salad'),
    path('add/platter/', views.shop_platter, name='shop-platter'),
    path('shopping-cart/', views.shopping_cart, name="shopping-cart"),
    path('order-items/', views.add_order_item, name="add-order-item"),
    path('view-cart/<str:access>/', views.show_shopping_cart, name='show-shopping-cart'),
    path('delete/shopping-item/<str:id>/', views.delete_shopping_item, name='delete-shopping-item'),
]