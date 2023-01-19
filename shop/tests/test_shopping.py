from django.test import TestCase, Client
from django.core.management import call_command
from base.models import User
from shop.models import Topping, Regular, Sicillian, Sub, Pasta, Salad, Platter


class SitePagesTestCase(TestCase):
    fixtures = ["testuser.json"]

    @classmethod
    def setUpTestData(cls):
        call_command("fooditems", ["--add"])
        # c = Client()

    def setUp(self):
        user = User.objects.get(email="test@gmail.com")
        self.client.login(email=user.email, password="123!@#QWE")

    def test_menu_page(self):
        # c = Client()
        # user = User.objects.get(email='test@gmail.com')
        # self.client.login(email=user.email, password='123!@#QWE')
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/index.html")

        self.assertContains(response, "Regular")
        self.assertContains(response, "Sicillian")
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Salad")
        self.assertContains(response, "Platter")
        self.assertContains(response, "Sub")
        self.assertContains(response, "Small")
        self.assertContains(response, "Large")
        self.assertContains(response, "Profile")
        self.assertContains(response, "Special")
        self.assertContains(response, "Cheese")
        self.assertContains(response, "+ Mushrooms")
        self.assertContains(response, "Special")
        self.assertContains(response, "Canadian Bacon")
        self.assertContains(response, "Chicken Parm")

    def test_empty_shopping_cart(self):
        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/shopping_list.html")
        self.assertContains(response, "No Items in Shopping Cart")
        self.assertNotContains(response, "Place Order")

    def test_regular_pizza_shopping_cart(self):

        toppings = Topping.objects.all()

        toppingOne = toppings[0].topping
        toppingTwo = toppings[1].topping
        toppingThree = toppings[2].topping
        small_price = str(Regular.objects.get(delicacy="3 Toppings").small)
        response = self.client.post(
            "/shop/add/pizza/",
            {
                "toppingOne": toppingOne,
                "toppingTwo": toppingTwo,
                "toppingThree": toppingThree,
                "small": small_price,
                "item": "Regular",
            },
            content_type="application/json",
        )

        data = response.json()

        response = self.client.post(
            "/shop/order-items/", data["message"], content_type="application/json"
        )

        # call_command("dumpdata", "shop.ShoppingCartItem")

        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/shopping_list.html")
        self.assertNotContains(response, "No Items in Shopping Cart")
        self.assertContains(response, "Regular")
        self.assertContains(response, "Pepperoni")
        self.assertContains(response, "16.95")

    def test_sicillian_pizza_shopping_cart(self):

        toppings = Topping.objects.all()

        toppingOne = toppings[0].topping
        toppingTwo = toppings[1].topping
        toppingThree = toppings[2].topping
        small_price = str(Sicillian.objects.get(delicacy="3 Items").small)
        response = self.client.post(
            "/shop/add/pizza/",
            {
                "toppingOne": toppingOne,
                "toppingTwo": toppingTwo,
                "toppingThree": toppingThree,
                "small": small_price,
                "item": "Sicillian",
            },
            content_type="application/json",
        )

        data = response.json()

        response = self.client.post(
            "/shop/order-items/", data["message"], content_type="application/json"
        )

        # call_command("dumpdata", "shop.ShoppingCartItem")

        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("shop/shopping_list.html", response.templates[0].name)
        self.assertNotIn(b"No Items in Shopping Cart", response.content)
        self.assertIn(b"Sicillian", response.content)
        self.assertIn(b"Pepperoni", response.content)
        self.assertIn(b"31.50", response.content)

    def test_sub_shopping_cart(self):

        sub = "Steak + Cheese"
        small_price = str(Sub.objects.get(sub=f"{sub}").small)
        mushroom_small = str(Sub.objects.get(sub="+ Mushrooms").small)
        peppers_small = str(Sub.objects.get(sub="+ Green Peppers").small)
        onions_small = str(Sub.objects.get(sub="+ Onions").small)
        response = self.client.post(
            "/shop/add/sub/",
            {
                "+ Mushrooms": mushroom_small,
                "+ Green Peppers": peppers_small,
                "+ Onions": onions_small,
                "small": small_price,
                "type": "Cheese + Steak",
                "item": "Sub Sandwich",
            },
            content_type="application/json",
        )

        data = response.json()

        response = self.client.post(
            "/shop/order-items/", data["message"], content_type="application/json"
        )

        # call_command("dumpdata", "shop.ShoppingCartItem")

        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("shop/shopping_list.html", response.templates[0].name)
        self.assertNotIn(b"No Items in Shopping Cart", response.content)
        self.assertIn(b"Sub Sandwich", response.content)
        self.assertIn(b"Cheese + Steak", response.content)
        self.assertIn(b"+ Mushrooms", response.content)
        self.assertIn(b"+ Green Peppers", response.content)
        self.assertIn(b"+ Onions", response.content)
        # total = str(float(mushroom_small)+ float(peppers_small) + float(onions_small) + float(small_price))
        self.assertIn(b"10.25", response.content)

    def test_pasta_shopping_cart(self):

        pasta = "Baked Ziti w/Chicken"
        fixed_price = str(Pasta.objects.get(pasta=f"{pasta}").fixed)

        response = self.client.post(
            "/shop/add/pasta/",
            {"Baked Ziti w/Chicken": fixed_price, "item": "Pasta"},
            content_type="application/json",
        )

        data = response.json()

        response = self.client.post(
            "/shop/order-items/", data["message"], content_type="application/json"
        )

        # call_command("dumpdata", "shop.ShoppingCartItem")

        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("shop/shopping_list.html", response.templates[0].name)
        self.assertNotIn(b"No Items in Shopping Cart", response.content)
        self.assertIn(b"Pasta", response.content)
        self.assertIn(b"Baked Ziti w/Chicken", response.content)
        self.assertIn(b"10.95", response.content)

    def test_salad_shopping_cart(self):

        salad = "Salad w/ Tuna"
        fixed_price = str(Salad.objects.get(salad=f"{salad}").fixed)

        response = self.client.post(
            "/shop/add/salad/",
            {"salad-Salad w/ Tuna": fixed_price, "item": "Salad"},
            content_type="application/json",
        )

        data = response.json()

        response = self.client.post(
            "/shop/order-items/", data["message"], content_type="application/json"
        )

        # call_command("dumpdata", "shop.ShoppingCartItem")

        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("shop/shopping_list.html", response.templates[0].name)
        self.assertNotIn(b"No Items in Shopping Cart", response.content)
        self.assertIn(b"Salad", response.content)
        self.assertIn(b"Salad w/ Tuna", response.content)
        self.assertIn(b"9.75", response.content)

    def test_platter_shopping_cart(self):

        platter = "Chicken Parm"
        small_price = str(Platter.objects.get(platter=f"{platter}").small)
        large_price = str(Platter.objects.get(platter=f"{platter}").large)

        response = self.client.post(
            "/shop/add/platter/",
            {
                "small": small_price,
                "large": large_price,
                "type": "Chicken Parm",
                "item": "Platter",
            },
            content_type="application/json",
        )

        data = response.json()

        response = self.client.post(
            "/shop/order-items/", data["message"], content_type="application/json"
        )

        # call_command("dumpdata", "shop.ShoppingCartItem")

        response = self.client.get("/shop/view-cart/page/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("shop/shopping_list.html", response.templates[0].name)
        self.assertNotIn(b"No Items in Shopping Cart", response.content)
        self.assertIn(b"Platter", response.content)
        self.assertIn(b"Chicken Parm", response.content)
        # total = str(float(mushroom_small)+ float(peppers_small) + float(onions_small) + float(small_price))
        self.assertIn(b"140.00", response.content)
