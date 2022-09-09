from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from order.models import OrderedItem
import time

from sqlalchemy import delete



def login_user(driver, timeout, server):
    driver.get('%s%s'%(server, '/user/login/'))
    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    sign_in = driver.find_element(By.XPATH, '//button[@type="submit"]')

    time.sleep(timeout)
    email.send_keys('test@gmail.com')
    time.sleep(timeout)
    password.send_keys('u555me666$!(') 
    time.sleep(timeout)
    sign_in.click()
    time.sleep(timeout)

def scroll_to_button_and_click(driver, button):
    time.sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3)
    button.click()

class TestOrdersChrome(StaticLiveServerTestCase):

    fixtures = ['users.json', 'shopping_cart.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()


    def test_view_shopping_cart_items(self):
        timeout = 5
        login_user(self.driver, timeout-4, self.live_server_url)
        time.sleep(3)
        self.driver.get('%s%s'%(self.live_server_url, '/shop/view-cart/page/'))
        


        self.assertIn('Regular', self.driver.page_source)
        self.assertIn('Pepperoni', self.driver.page_source)
        self.assertIn('16.95', self.driver.page_source)

        self.assertIn('Sicillian', self.driver.page_source)
        self.assertIn('Pepperoni', self.driver.page_source)
        self.assertIn('31.50', self.driver.page_source)

        self.assertIn('Sub Sandwich', self.driver.page_source)
        self.assertIn('Cheese + Steak', self.driver.page_source)
        self.assertIn('+ Mushrooms', self.driver.page_source)
        self.assertIn('+ Green Peppers', self.driver.page_source)
        self.assertIn('+ Onions', self.driver.page_source)
        # total = str(float(mushroom_small)+ float(peppers_small) + float(onions_small) + float(small_price))
        self.assertIn('10.25', self.driver.page_source)
        self.assertIn('Pasta', self.driver.page_source)
        self.assertIn('Baked Ziti w/Chicken', self.driver.page_source)                
        self.assertIn('10.95', self.driver.page_source)

        self.assertIn('Salad', self.driver.page_source)
        self.assertIn('Salad w/ Tuna', self.driver.page_source)                
        self.assertIn('9.75', self.driver.page_source)

        self.assertIn('Platter', self.driver.page_source)        
        self.assertIn('Chicken Parm', self.driver.page_source)        
        # total = str(float(mushroom_small)+ float(peppers_small) + float(onions_small) + float(small_price))
        self.assertIn('140.00', self.driver.page_source)

        self.assertIn('Place Order', self.driver.page_source)
        self.assertIn('View Orders', self.driver.page_source)

        time.sleep(3)
        
        
        view_orders_button = self.driver.find_element(By.LINK_TEXT, 'View Orders')
        scroll_to_button_and_click(self.driver, view_orders_button)

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ordered-items'))
        )
        self.assertIn('No Previously Ordered Items', self.driver.page_source)

    def test_delete_item_from_cart(self):
        """Delete item from cart"""
        timeout = 5

        login_user(self.driver, timeout-4, self.live_server_url)
        time.sleep(3)
        self.driver.get('%s%s'%(self.live_server_url, '/shop/view-cart/page/'))

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#shopping-cart-table'))
        )

        self.assertIn('Regular', self.driver.page_source)
        self.assertIn('Pepperoni', self.driver.page_source)
        self.assertIn('16.95', self.driver.page_source)

        
        ActionChains(self.driver).scroll(0, 0, 0, 100, 5, origin="viewport")
        delete_item_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.btn-delete-cart-item')
        delete_item_buttons[3].click()

        
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='delete-item']"))
        )
        time.sleep(4)
        confirm_delete_button = self.driver.find_element(By.XPATH, "//button[@id='delete-item']")
        confirm_delete_button.click()

        time.sleep(2)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='confirm-action']"))
        )

        confirm_button = self.driver.find_element(By.XPATH, "//button[@id='confirm-action']")
        confirm_button.click()
        time.sleep(5)

        self.assertNotIn('Salad', self.driver.page_source)
        self.assertNotIn('Salad w/ Tuna', self.driver.page_source)                
        self.assertNotIn('9.75', self.driver.page_source)

    def test_place_order_from_cart(self):
        """Place order from cart"""

        timeout = 5

        login_user(self.driver, timeout-4, self.live_server_url)
        time.sleep(3)
        self.driver.get('%s%s'%(self.live_server_url, '/shop/view-cart/page/'))

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#place-order'))
        )

        place_order_button = self.driver.find_element(By.CSS_SELECTOR, '#place-order')
        scroll_to_button_and_click(self.driver, place_order_button)

        time.sleep(5)

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#add-orders'))
        )

        add_order_button = self.driver.find_element(By.CSS_SELECTOR, '#add-orders')
        scroll_to_button_and_click(self.driver, add_order_button)

        time.sleep(2)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='confirm-action']"))
        )

        confirm_button = self.driver.find_element(By.XPATH, "//button[@id='confirm-action']")
        confirm_button.click()
        time.sleep(10)

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'View Menu'))
        )


        self.assertNotIn('Regular', self.driver.page_source)
        self.assertNotIn('Pepperoni', self.driver.page_source)
        self.assertNotIn('16.95', self.driver.page_source)

        self.assertNotIn('Sicillian', self.driver.page_source)
        self.assertNotIn('Pepperoni', self.driver.page_source)
        self.assertNotIn('31.50', self.driver.page_source)

        self.assertNotIn('Sub Sandwich', self.driver.page_source)
        self.assertNotIn('Cheese + Steak', self.driver.page_source)
        self.assertNotIn('+ Mushrooms', self.driver.page_source)
        self.assertNotIn('+ Green Peppers', self.driver.page_source)
        self.assertNotIn('+ Onions', self.driver.page_source)
        # total = str(float(mushroom_small)+ float(peppers_small) + float(onions_small) + float(small_price))
        self.assertNotIn('10.25', self.driver.page_source)
        self.assertNotIn('Pasta', self.driver.page_source)
        self.assertNotIn('Baked Ziti w/Chicken', self.driver.page_source)                
        self.assertNotIn('10.95', self.driver.page_source)

        self.assertNotIn('Salad', self.driver.page_source)
        self.assertNotIn('Salad w/ Tuna', self.driver.page_source)                
        self.assertNotIn('9.75', self.driver.page_source)

        self.assertNotIn('Platter', self.driver.page_source)        
        self.assertNotIn('Chicken Parm', self.driver.page_source)        
        # total = str(float(mushroom_small)+ float(peppers_small) + float(onions_small) + float(small_price))
        self.assertNotIn('140.00', self.driver.page_source)

        self.assertIn('View Menu', self.driver.page_source)
        self.assertIn('Place Order', self.driver.page_source)

        view_orders_button = self.driver.find_element(By.LINK_TEXT, 'View Orders')
        scroll_to_button_and_click(self.driver, view_orders_button)

        time.sleep(5)

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ordered-items'))
        )

        ordered_item = OrderedItem.objects.filter(food_item="Pasta")
        self.assertTrue(ordered_item.exists())

        filter_placed_button = self.driver.find_element(By.CSS_SELECTOR, '#placed')
        filter_placed_button.click()

        time.sleep(3)
        ordered_item = OrderedItem.objects.filter(food_item="Pasta")
        self.assertTrue(ordered_item.exists())        

        time.sleep(3)

        filter_cooking_button = self.driver.find_element(By.CSS_SELECTOR, '#cooking')
        filter_cooking_button.click()

        time.sleep(3)
        
        self.assertNotIn('Regular', self.driver.page_source)
        self.assertNotIn('Pepperoni', self.driver.page_source)        

        self.assertNotIn('Sicillian', self.driver.page_source)
        self.assertNotIn('Pepperoni', self.driver.page_source)
        

        self.assertNotIn('Sub Sandwich', self.driver.page_source)
        self.assertNotIn('Cheese + Steak', self.driver.page_source)
        self.assertNotIn('+ Mushrooms', self.driver.page_source)
        self.assertNotIn('+ Green Peppers', self.driver.page_source)
        self.assertNotIn('+ Onions', self.driver.page_source)
        
        self.assertNotIn('Pasta', self.driver.page_source)
        self.assertNotIn('Baked Ziti w/Chicken', self.driver.page_source)                        

        self.assertNotIn('Salad', self.driver.page_source)
        self.assertNotIn('Salad w/ Tuna', self.driver.page_source)                

        self.assertNotIn('Platter', self.driver.page_source)        
        self.assertNotIn('Chicken Parm', self.driver.page_source)        

        self.assertIn('No Previously Ordered Items', self.driver.page_source)