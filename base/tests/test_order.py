from django.test import TestCase, Client 
from django.core.management import call_command
from base.models import User, OrderedItem



class OrderTestCase(TestCase):
    fixtures = ['users.json', 'shopping_cart.json']
    def setUp(self):        
        
        call_command("fooditems", ['--add'])        
        user = User.objects.get(email='test@gmail.com')
        self.client.login(email=user.email, password='u555me666$!(')


                    
    def test_order_list(self):
        
        # self.assertTrue(authenticated)
        response = self.client.get("/view/show-ordered-items/retrieve/", follow=True)
        self.assertEqual(response.status_code, 200)        
        self.assertIn("base/ordered_list.html", response.templates[0].name)

    def test_order_shopping_items(self):

        response = self.client.post('/shop/order-items/')
        self.assertEqual('Success', response.json()['message'])
        
        pasta_order = OrderedItem.objects.filter(food_item="Pasta", choices="Baked Ziti w/Chicken", price="10.95")
        self.assertTrue(pasta_order.exists())
        platter_order = OrderedItem.objects.filter(food_item="Platter (small + large)", choices="Chicken Parm", price="140.00")
        self.assertTrue(platter_order.exists())
        regular_order = OrderedItem.objects.filter(food_item="Regular (small)", choices="Topping(s): Pepperoni, Sausage, Mushrooms", price="16.95")
        self.assertTrue(regular_order.exists())
        salad_order = OrderedItem.objects.filter(food_item="Salad", choices="Salad w/ Tuna", price="9.75")
        self.assertTrue(salad_order.exists())
        sicillian_order = OrderedItem.objects.filter(food_item="Sicillian (small)", choices="Topping(s): Pepperoni, Sausage, Mushrooms", price="31.50")
        self.assertTrue(sicillian_order.exists())
        sub_order = OrderedItem.objects.filter(food_item="Sub Sandwich (small)", choices="Cheese + Steak + Mushrooms + Green Peppers + Onions", price="10.25")
        self.assertTrue(sub_order.exists())
        # self.assertIn(b"Platter (small + large)", response.content)
        # self.assertIn(b"Regular (small)", response.content)
        # self.assertIn(b"Salad", response.content)
        # self.assertIn(b"Sicillian (small)", response.content)
        # self.assertIn(b"Sub Sandwich (small)", response.content)