from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('order/<str:food_order>/<str:id>/', views.get_order_item, name="food-order"),
    path('order-special/<str:pizza>/', views.get_special, name='shop-special'),

    path('shop/add/pizza/', views.shop_pizza, name='shop-pizza'),
    path('shop/add/sub/', views.shop_sub, name='shop-sub'),
    path('shop/add/pasta/', views.shop_pasta, name='shop-pasta'),
    path('shop/add/salad/', views.shop_salad, name='shop-salad'),
    path('shop/add/platter/', views.shop_platter, name='shop-platter'),
    path('shop/shopping-cart/', views.shopping_cart, name="shopping-cart"),
    path('shop/add-order-item/', views.add_order_item, name="add-order-item"),
    path('shop/order-items/', views.order_shopping_items, name='order-shopping-items'),


    path('view/shopping-cart/<str:access>/', views.show_shopping_cart, name='show-shopping-cart'),
    path('view/show-ordered-items/<str:status>/', views.show_ordered_items, name='show-ordered-items'),

    path('delete/shopping-item/<str:id>/', views.delete_shopping_item, name='delete-shopping-item'),
    path('delete/delivered-orders/', views.delete_delivered_orders, name='delete-delivered-orders'),

    path('user/login/', views.login_user, name='login-user'),
    path('user/logout/', views.logout_user, name='logout-user'),    
    path('user/register/', views.register_user, name='register-user'),    
    path('user/profile/<str:action>/', views.get_user_profile, name='user-profile'),
]