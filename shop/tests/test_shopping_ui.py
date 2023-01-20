from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time


def login_user(driver, timeout, server):
    driver.get("%s%s" % (server, "/user/login/"))
    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    sign_in = driver.find_element(By.XPATH, '//button[@type="submit"]')

    time.sleep(timeout)
    email.send_keys("test@gmail.com")
    time.sleep(timeout)
    password.send_keys("123!@#QWE")
    time.sleep(timeout)
    sign_in.click()
    time.sleep(timeout)


def scroll_to_menu_button(actions, driver, button):

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    actions.move_to_element(button)
    actions.click()
    actions.perform()
    time.sleep(5)


def scroll_to_shop_button_and_click(driver, x, y, actions, button):
    if y != 0:
        actions.scroll(0, 0, x, y, 5, origin="viewport")
        actions.perform()
    else:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight - (window.innerHeight + (window.innerHeight/2)))"
        )
        time.sleep(3)
        # actions.move_to_element(button)
        # actions.perform()
    time.sleep(2)
    button.click()
    time.sleep(5)


def view_cart(driver):
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".shopping-cart"))
    )
    shopping_cart_button = driver.find_element(By.CSS_SELECTOR, ".shopping-cart")
    shopping_cart_button.click()
    time.sleep(3)


def confirm_shopping_item(driver):
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#add"))
    )
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#add").click()
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#confirm"))
    )
    time.sleep(3)
    confirm_item_button = driver.find_element(By.CSS_SELECTOR, "#confirm")
    confirm_item_button.click()


class TestShoppingChrome(StaticLiveServerTestCase):

    fixtures = [
        "regular.json",
        "sicillian.json",
        "topping.json",
        "sub.json",
        "pasta.json",
        "salad.json",
        "platter.json",
        "specialregular.json",
        "specialsicillian.json",
        "testuser.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def test_shopping_pizza(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # Pizza
        sicillian_buttons = self.driver.find_elements(
            By.CSS_SELECTOR, ".pizza-sicillian-button"
        )

        time.sleep(5)

        scroll_to_shop_button_and_click(
            self.driver, 0, 600, ActionChains(self.driver), sicillian_buttons[2]
        )

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='sicillian-form']"))
        )
        input_one = self.driver.find_element(By.XPATH, "//input[@id='toppingOne']")
        input_one.clear()
        option_one = self.driver.find_element(
            By.XPATH, "//datalist[@id='topping1-options']/option[2]"
        )
        input_one.send_keys(option_one.get_attribute("value"))

        input_two = self.driver.find_element(By.XPATH, "//input[@id='toppingTwo']")
        input_two.clear()
        option_two = self.driver.find_element(
            By.XPATH, "//datalist[@id='topping1-options']/option[4]"
        )
        input_two.send_keys(option_two.get_attribute("value"))

        large_selection = self.driver.find_element(By.XPATH, "//input[@id='large']")
        large_selection.click()

        confirm_shopping_item(self.driver)

        view_cart(self.driver)

        self.assertIn("Sicillian", self.driver.page_source)

    def test_shopping_sub(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # Sub

        sub = self.driver.find_element(By.XPATH, "//h2[@id='headingTwo']")
        actions = ActionChains(self.driver, 5)
        scroll_to_menu_button(actions, self.driver, sub)

        sub_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".sub-button")
        scroll_to_shop_button_and_click(
            self.driver, 0, 0, ActionChains(self.driver), sub_buttons[9]
        )

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='sub-form']"))
        )

        large_selection = self.driver.find_element(By.XPATH, "//input[@id='large']")
        large_selection.click()

        mushrooms_selection = self.driver.find_element(
            By.XPATH, "//input[@id='mushrooms']"
        )
        mushrooms_selection.click()

        onions_selection = self.driver.find_element(By.XPATH, "//input[@id='onions']")
        onions_selection.click()

        cheese_selection = self.driver.find_element(By.XPATH, "//input[@id='cheese']")
        cheese_selection.click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        confirm_shopping_item(self.driver)
        # View Cart

        view_cart(self.driver)

        self.assertIn("Sub", self.driver.page_source)
        self.assertIn("+ Mushrooms", self.driver.page_source)

    def test_shopping_pasta(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # pasta

        pasta = self.driver.find_element(By.XPATH, "//h2[@id='headingThree']")
        actions = ActionChains(self.driver, 5)
        scroll_to_menu_button(actions, self.driver, pasta)

        pasta_button = self.driver.find_element(By.CSS_SELECTOR, "#pasta-button")
        scroll_to_shop_button_and_click(
            self.driver, 0, 500, ActionChains(self.driver), pasta_button
        )

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='pasta-form']"))
        )

        pasta_selection = self.driver.find_element(
            By.XPATH, "//input[@id='meatballs-price']"
        )
        pasta_selection.click()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        confirm_shopping_item(self.driver)
        # View Cart

        view_cart(self.driver)

        self.assertIn("Pasta", self.driver.page_source)

    def test_shopping_salad(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # salad

        salad = self.driver.find_element(By.XPATH, "//h2[@id='headingFour']")
        actions = ActionChains(self.driver, 5)
        scroll_to_menu_button(actions, self.driver, salad)

        salad_button = self.driver.find_element(By.CSS_SELECTOR, "#salad-button")
        scroll_to_shop_button_and_click(
            self.driver, 0, 500, ActionChains(self.driver), salad_button
        )

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='salad-form']"))
        )

        salad_selection = self.driver.find_element(By.XPATH, "//input[@id='antipasto']")
        salad_selection.click()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        confirm_shopping_item(self.driver)
        # View Cart

        view_cart(self.driver)

        self.assertIn("Salad", self.driver.page_source)

    def test_shopping_platter(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # platter

        platter = self.driver.find_element(By.XPATH, "//h2[@id='headingFive']")
        actions = ActionChains(self.driver, 5)
        scroll_to_menu_button(actions, self.driver, platter)

        platter_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".platter-button")
        scroll_to_shop_button_and_click(
            self.driver, 0, 500, ActionChains(self.driver), platter_buttons[2]
        )

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='platter-form']"))
        )

        large_selection = self.driver.find_element(By.XPATH, "//input[@id='large']")
        large_selection.click()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        confirm_shopping_item(self.driver)
        # View Cart

        view_cart(self.driver)

        self.assertIn("Platter", self.driver.page_source)

    def test_shopping_special_regular(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # special regular

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#order-special-regular"))
        )

        special_regular = self.driver.find_element(
            By.CSS_SELECTOR, "#order-special-regular"
        )
        special_regular.click()

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='regular-form']"))
        )

        large_selection = self.driver.find_element(By.XPATH, "//input[@id='large']")
        large_selection.click()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        confirm_shopping_item(self.driver)
        # View Cart

        view_cart(self.driver)

        self.assertIn("Special", self.driver.page_source)

    def test_shopping_special_sicillian(self):
        timeout = 5

        login_user(self.driver, timeout - 4, self.live_server_url)

        # special sicillian

        try:
            special_sicillian = self.driver.find_element(
                By.CSS_SELECTOR, "#order-special-sicillian"
            )
            special_sicillian.click()
        except ElementClickInterceptedException:
            # WebDriverWait(self.driver, 60, 2, ElementClickInterceptedException).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, '#order-special-sicillian'))
            # )
            special_sicillian = self.driver.find_element(
                By.CSS_SELECTOR, "#order-special-sicillian"
            )
            special_sicillian.click()

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='sicillian-form']"))
        )

        large_selection = self.driver.find_element(By.XPATH, "//input[@id='large']")
        large_selection.click()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        confirm_shopping_item(self.driver)
        # View Cart

        view_cart(self.driver)

        self.assertIn("Special", self.driver.page_source)
