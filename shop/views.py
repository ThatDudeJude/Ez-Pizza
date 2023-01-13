from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import (
    Pasta,
    Platter,
    Salad,
    Sicillian,
    Topping,
    Regular,
    Sub,
    ShoppingCartItem,
    SpecialSicillian,
    SpecialRegular,
)

from django.contrib.auth.decorators import login_required
from functools import reduce
import json

# Create your views here.


@login_required(login_url="/user/login/")
def get_special(request, pizza):
    if pizza == "regular":
        order = SpecialRegular.objects.first()
        order_data = {
            "small": order.small,
            "large": order.large,
            "delicacy": order.delicacy,
            "special": True,
        }
        response = {"data": order_data, "toppings": None, "name": "Regular Pizza"}
    elif pizza == "sicillian":
        order = SpecialSicillian.objects.first()
        order_data = {
            "small": order.small,
            "large": order.large,
            "delicacy": order.delicacy,
            "special": True,
        }
        response = {"data": order_data, "toppings": None, "name": "Sicillian Pizza"}

    return JsonResponse(response, safe=False)


@login_required(login_url="/user/login/")
def get_order_item(request, food_order, id):
    if food_order == "regular":
        order = Regular.objects.get(pk=id)
        if order.delicacy == "Special":
            order = SpecialRegular.objects.first()
            order_data = {
                "small": order.small,
                "large": order.large,
                "delicacy": order.delicacy,
                "special": True,
            }
        else:
            order_data = {
                "small": order.small,
                "large": order.large,
                "delicacy": order.delicacy,
                "special": False,
            }
        toppings = [
            {"id": topping.id, "name": topping.topping}
            for topping in Topping.objects.all()
        ]
        response = {"data": order_data, "toppings": toppings, "name": "Regular Pizza"}

    elif food_order == "sicillian":
        order = Sicillian.objects.get(pk=id)
        if order.delicacy == "Special":
            order = SpecialSicillian.objects.first()
            order_data = {
                "small": order.small,
                "large": order.large,
                "delicacy": order.delicacy,
                "special": True,
            }
        else:
            order_data = {
                "small": order.small,
                "large": order.large,
                "delicacy": order.delicacy,
                "special": False,
            }
        toppings = [
            {"id": topping.id, "name": topping.topping}
            for topping in Topping.objects.all()
        ]
        response = {"data": order_data, "toppings": toppings, "name": "Sicillian Pizza"}

    elif food_order == "subs":
        order = Sub.objects.get(pk=id)
        order_data = {"small": order.small, "large": order.large, "sub": order.sub}
        response = {"data": order_data, "name": "Sub Sandwich"}

    elif food_order == "pastas":
        orders = Pasta.objects.all()
        response = {"name": "Pasta", "data": []}
        for order in orders:
            response["data"].append({"delicacy": order.pasta, "fixed": order.fixed})

    elif food_order == "salads":
        orders = Salad.objects.all()
        response = {"name": "Salad", "data": []}
        for order in orders:
            response["data"].append({"delicacy": order.salad, "fixed": order.fixed})

    elif food_order == "platters":
        order = Platter.objects.get(pk=id)
        order_data = {
            "small": order.small,
            "large": order.large,
            "platter": order.platter,
        }
        response = {"data": order_data, "name": "Dinner Platter"}

    return JsonResponse(response, safe=False)


@login_required(login_url="/user/login/")
def shop_pizza(request):

    if request.method == "POST":
        form_data = json.load(request)
        food = form_data["item"]
        size = f"{' + '.join([f'{key}' for key in form_data.keys() if key == 'small' or key =='large'])}"
        price = "%.2f" % reduce(
            lambda a, b: a + b,
            [
                float(form_data[key])
                for key in form_data.keys()
                if key == "small" or key == "large"
            ],
        )
        if form_data.get("type"):
            info = f"{form_data.get('special', '')}{form_data['type']}"
        else:
            info = f"Topping(s): {', '.join([f'{form_data[key]}' for key in form_data.keys() if key.startswith('topping')])}"
        response = {"food": food + f" ({size})", "info": info, "price": price}
        return JsonResponse({"error": False, "message": response})

    return JsonResponse({"error": True, "message": "Something went wrong!"})


@login_required(login_url="/user/login/")
def shop_sub(request):

    if request.method == "POST":
        form_data = json.load(request)
        food = form_data["item"]
        size = f"{' + '.join([f'{key}' for key in form_data.keys() if key == 'small' or key =='large'])}"
        price = "%.2f" % reduce(
            lambda a, b: a + b,
            [
                float(form_data[key])
                for key in form_data.keys()
                if key == "small" or key == "large" or key.startswith("+")
            ],
        )
        info = f"{form_data['type']} " + " ".join(
            [f"{extra}" for extra in form_data.keys() if extra.startswith("+")]
        )
        response = {"food": food + f" ({size})", "info": info, "price": price}
        return JsonResponse({"error": False, "message": response})

    return redirect("index")


@login_required(login_url="/user/login/")
def shop_pasta(request):

    if request.method == "POST":
        form_data = json.load(request)
        food = form_data["item"]
        price = "%.2f" % reduce(
            lambda a, b: a + b,
            [
                float(form_data[key])
                for key in form_data.keys()
                if key.startswith("Baked")
            ],
        )
        info = ", ".join(
            [f"{key}" for key in form_data.keys() if key.startswith("Baked")]
        )
        response = {"food": food, "info": info, "price": price}
        return JsonResponse({"error": False, "message": response})

    return redirect("index")


@login_required(login_url="/user/login/")
def shop_salad(request):

    if request.method == "POST":
        form_data = json.load(request)
        food = form_data["item"]
        price = "%.2f" % reduce(
            lambda a, b: a + b,
            [
                float(form_data[key])
                for key in form_data.keys()
                if key.startswith("salad")
            ],
        )
        info = ", ".join(
            [
                f'{key.split("-")[1]}'
                for key in form_data.keys()
                if key.startswith("salad-")
            ]
        )
        response = {"food": food, "info": info, "price": price}
        return JsonResponse({"error": False, "message": response})

    return redirect("index")


@login_required(login_url="/user/login/")
def shop_platter(request):

    if request.method == "POST":
        form_data = json.load(request)
        food = form_data["item"]
        size = f"{' + '.join([f'{key}' for key in form_data.keys() if key == 'small' or key =='large'])}"
        price = "%.2f" % reduce(
            lambda a, b: a + b,
            [
                float(form_data[key])
                for key in form_data.keys()
                if key == "small" or key == "large"
            ],
        )
        info = f"{form_data['type']}"
        response = {"food": food + f" ({size})", "info": info, "price": price}
        return JsonResponse({"error": False, "message": response})

    return redirect("index")


@login_required(login_url="/user/login/")
def shopping_cart(request):
    shopping_items = ShoppingCartItem.objects.filter(client=request.user).count()
    return JsonResponse({"totalItems": shopping_items})


@login_required(login_url="/user/login/")
def add_order_item(request):

    if request.method == "POST":
        order_data = json.load(request)
        new_order = ShoppingCartItem(
            client=request.user,
            food_item=order_data["food"],
            choices=order_data["info"],
            price=order_data["price"],
        )
        new_order.save()
    return redirect("index")


@login_required(login_url="/user/login/")
def get_shopping_cart_data(request):
    shopping_cart = ShoppingCartItem.objects.filter(client=request.user)
    total_price = 0
    shopping_cart_items = []
    for item in shopping_cart.values():
        total_price += float(item["price"])
        shopping_cart_items.append(item)
    context = {
        "shopping_cart": shopping_cart_items,
        "total_price": "%.2f" % total_price,
    }
    return context


@login_required(login_url="/user/login/")
def show_shopping_cart(request, access="denied"):
    if request.user.is_authenticated:
        context = get_shopping_cart_data(request)
        if access == "page":
            return render(request, "shop/shopping_list.html", context)
        elif access == "data":
            return JsonResponse(context)


@login_required(login_url="/user/login/")
def delete_shopping_item(request, id):

    if request.user.is_authenticated and request.method == "DELETE":
        try:
            shopping_cart_item = ShoppingCartItem.objects.get(pk=id)
            shopping_cart_item.delete()

            return JsonResponse({"error": False, "message": "Deleted from Cart"})
        except:

            return JsonResponse({"error": True, "message": "Something went wrong"})

    shopping_cart_item = ShoppingCartItem.objects.get(pk=id)
    data = {
        "action": "delete",
        "food_item": shopping_cart_item.food_item,
        "choices": shopping_cart_item.choices,
        "price": shopping_cart_item.price,
    }
    return JsonResponse(data)
