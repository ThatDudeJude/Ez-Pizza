import smtplib
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags import humanize
from django.http import JsonResponse
from django.urls import reverse
from .models import OrderedItem
from base.models import User
from .order_token import generate_order_token
from shop.models import ShoppingCartItem
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.


def send_order_email(request, send_mail, client, orders, token, template):
    protocol = "https" if request.is_secure() else "http"
    subject = "Placed Orders on EzPizza"
    recepient_name = client["name"]
    uid = urlsafe_base64_encode(force_bytes(request.user.id))
    context = {
        "username": recepient_name,
        "ordered_items": orders,
        "time": orders[-1].created,
        "domain": request.get_host(),
        "protocol": protocol,
        "uid": uid,
        "token": token,
    }
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = "gachjude@gmail.com"
    to = client["email"]

    send_mail(subject, html_message, from_email, [to], html_message=html_message)


@login_required(login_url="/user/login/")
def order_shopping_items(request):
    if request.user.is_authenticated and request.method == "POST":
        try:
            latest_orders = []
            item_prices = []
            ordering_client = {"name": request.user.name, "email": request.user.email}
            shopping_cart = ShoppingCartItem.objects.filter(client=request.user)
            for item in shopping_cart:
                order_item = OrderedItem(
                    client=request.user,
                    food_item=item.food_item,
                    choices=item.choices,
                    price=item.price,
                )

                order_item.save()
                latest_orders.append(order_item)
                item_prices.append(str(order_item.price))
                item.delete()

            # Create order token
            generate_order_token.create_token(request.user, item_prices)
            send_order_email(
                request,
                mail.send_mail,
                ordering_client,
                latest_orders,
                generate_order_token.token,
                "order/order_email_template.html",
            )
            return JsonResponse(
                {
                    "error": False,
                    "message": "Order Completed",
                    "email": str(request.user.email),
                }
            )
        except (smtplib.SMTPException):
            print("ordering from cart went wrong")
            return JsonResponse({"error": True, "message": "Something went wrong"})
    return redirect("show_ordered_items", status="ALL")


def get_time(created):
    return humanize.naturaltime(created)


@login_required(login_url="/user/login/")
def show_ordered_items_from_email_link(request, uidb64, token):
    if request.method == "GET":
        id = urlsafe_base64_decode(uidb64)
        print("id", id)
        try:
            user = User.objects.get(pk=id)
            if generate_order_token.check_token(token) and user == request.user:
                print("Showing ")
                return redirect("show-ordered-items", status="retrieve")

        except ValueError:
            return render(request, "error.html", {"message": "Bad request!"})


@login_required(login_url="/user/login/")
def show_ordered_items(request, status):

    if request.user.is_authenticated:
        if status == "retrieve":
            ordered_items = OrderedItem.objects.filter(status="DELIVERED")
            return render(
                request,
                "order/ordered_list.html",
                {"has_delivered": len(ordered_items) > 0},
            )
        elif status.lower() != "all":
            ordered_items = (
                OrderedItem.objects.filter(client=request.user)
                .filter(status=f"{status.upper()}")
                .order_by("-created")
            )
        else:
            ordered_items = OrderedItem.objects.filter(client=request.user).order_by(
                "-created"
            )
        items = []
        for item in ordered_items.values():
            # item['created'] = item.get_time
            item["human_time"] = get_time(item["created"])
            items.append(item)
        return JsonResponse(items, safe=False)
    return redirect("index")


@login_required(login_url="/user/login/")
def delete_delivered_orders(request):
    if request.user.is_authenticated:
        OrderedItem.objects.filter(client=request.user).filter(
            status="DELIVERED"
        ).delete()

    return redirect("show-ordered-items", status="retrieve")
