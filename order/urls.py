from django.urls import path
from . import views

urlpatterns = [ 
    path('add-cart-items/', views.order_shopping_items, name='order-shopping-items'),
    path('view/show-orders/<str:status>/', views.show_ordered_items, name='show-ordered-items'),
    path('delete/delivered/', views.delete_delivered_orders, name='delete-delivered-orders'),
]