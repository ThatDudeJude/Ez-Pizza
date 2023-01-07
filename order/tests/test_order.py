from django.test import TestCase, Client
from django.core.management import call_command
from base.models import User
from order.models import OrderedItem
from django.core import mail
from django.urls import reverse
import re


class OrderTestCase(TestCase):
    fixtures = ["testuser.json", "shopping_cart.json"]

    @classmethod
    def setUpTestData(cls):
        call_command("fooditems", ["--add"])

    def setUp(self):
        user = User.objects.get(email="test@gmail.com")
        self.client.login(email=user.email, password="123!@#QWE")

    def test_order_list(self):

        # self.assertTrue(authenticated)
        response = self.client.get("/order/view/show-orders/retrieve/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/ordered_list.html")

    def test_order_shopping_items(self):

        response = self.client.post("/order/add-cart-items/")
        self.assertEqual("Order Completed", response.json()["message"])

        pasta_order = OrderedItem.objects.filter(
            food_item="Pasta", choices="Baked Ziti w/Chicken", price="10.95"
        )
        self.assertTrue(pasta_order.exists())
        platter_order = OrderedItem.objects.filter(
            food_item="Platter (small + large)", choices="Chicken Parm", price="140.00"
        )
        self.assertTrue(platter_order.exists())
        regular_order = OrderedItem.objects.filter(
            food_item="Regular (small)",
            choices="Topping(s): Pepperoni, Sausage, Mushrooms",
            price="16.95",
        )
        self.assertTrue(regular_order.exists())
        salad_order = OrderedItem.objects.filter(
            food_item="Salad", choices="Salad w/ Tuna", price="9.75"
        )
        self.assertTrue(salad_order.exists())
        sicillian_order = OrderedItem.objects.filter(
            food_item="Sicillian (small)",
            choices="Topping(s): Pepperoni, Sausage, Mushrooms",
            price="31.50",
        )
        self.assertTrue(sicillian_order.exists())
        sub_order = OrderedItem.objects.filter(
            food_item="Sub Sandwich (small)",
            choices="Cheese + Steak + Mushrooms + Green Peppers + Onions",
            price="10.25",
        )
        self.assertTrue(sub_order.exists())

    def test_send_email(self):
        self.client.post("/order/add-cart-items/")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Placed Orders on EzPizza")

        mail_body = mail.outbox[0].body

        args = (
            re.search("[\S\s]+(?<=/order/view/)([\S]+)/", mail_body).group(1).split("/")
        )

        uid = args[0]
        token = args[1]

        response = self.client.get(
            "%s"
            % reverse(
                "show-ordered-items-from-email", kwargs={"uidb64": uid, "token": token}
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/ordered_list.html")

        pasta_order = OrderedItem.objects.filter(
            food_item="Pasta", choices="Baked Ziti w/Chicken", price="10.95"
        )
        self.assertTrue(pasta_order.exists())
        platter_order = OrderedItem.objects.filter(
            food_item="Platter (small + large)", choices="Chicken Parm", price="140.00"
        )
        self.assertTrue(platter_order.exists())
        regular_order = OrderedItem.objects.filter(
            food_item="Regular (small)",
            choices="Topping(s): Pepperoni, Sausage, Mushrooms",
            price="16.95",
        )
        self.assertTrue(regular_order.exists())
        salad_order = OrderedItem.objects.filter(
            food_item="Salad", choices="Salad w/ Tuna", price="9.75"
        )
        self.assertTrue(salad_order.exists())
        sicillian_order = OrderedItem.objects.filter(
            food_item="Sicillian (small)",
            choices="Topping(s): Pepperoni, Sausage, Mushrooms",
            price="31.50",
        )
        self.assertTrue(sicillian_order.exists())
        sub_order = OrderedItem.objects.filter(
            food_item="Sub Sandwich (small)",
            choices="Cheese + Steak + Mushrooms + Green Peppers + Onions",
            price="10.25",
        )
        self.assertTrue(sub_order.exists())
