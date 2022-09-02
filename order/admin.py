from django.contrib import admin
from .models import OrderedItem
# Register your models here.

@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display=['client', 'food_item', 'choices', 'price', 'get_time', 'status']
    list_filter=['client', 'created', 'status']
    ordering = ['-created']