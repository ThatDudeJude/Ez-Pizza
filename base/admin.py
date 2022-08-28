from csv import list_dialects
from django.contrib import admin
from .models import Topping, User, Regular, Sicillian, Sub, Platter, Pasta, Salad, OrderedItem, ShoppingCartItem, SpecialRegular, SpecialSicillian

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']
    ordering = ["id"]

@admin.register(Regular)
class RegularAdmin(admin.ModelAdmin):
    list_display = ("delicacy", "small", "large")
    ordering = ["id"]

@admin.register(SpecialRegular)
class SpecialRegularAdmin(admin.ModelAdmin):
    list_display = ("delicacy", "small", "large")
    ordering = ["id"]

@admin.register(Sicillian)
class SicillianAdmin(admin.ModelAdmin):
    list_display = ("delicacy", "small", "large")
    ordering = ["id"]

@admin.register(SpecialSicillian)
class SpecialSicillianAdmin(admin.ModelAdmin):
    list_display = ("delicacy", "small", "large")
    ordering = ["id"]

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['topping']
    ordering = ["id"]

@admin.register(Sub)
class SubAdmin(admin.ModelAdmin):
    list_display = ['sub', 'small', 'large']
    ordering = ["id"]

@admin.register(Pasta)
class PastaAdmin(admin.ModelAdmin):
    list_display = ['pasta', 'fixed']
    ordering = ["id"]

@admin.register(Salad)
class SaladAdmin(admin.ModelAdmin):
    list_display = ['salad', 'fixed']
    ordering = ["id"]


@admin.register(Platter)
class PlatterAdmin(admin.ModelAdmin):
    list_display = ['platter', 'small', 'large']
    ordering = ['id']

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display=['client', 'food_item', 'choices', 'price', 'created']
    list_filter=['client', 'created']
    ordering = ['-created']

@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display=['client', 'food_item', 'choices', 'price', 'get_time', 'status']
    list_filter=['client', 'created', 'status']
    ordering = ['-created']