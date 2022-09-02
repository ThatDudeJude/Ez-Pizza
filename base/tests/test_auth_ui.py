from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from base.models import User
import time

def scroll_to_menu_button(actions, driver, button):
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)        
    actions.move_to_element(button)
    actions.click()        
    actions.perform()
    time.sleep(5)

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


class TestAuthenticationChrome(StaticLiveServerTestCase):
    fixtures = ['regular.json', 'sicillian.json', 'topping.json', 'sub.json', 
                'pasta.json', 'salad.json', 'platter.json', 'specialregular.json',
                'specialsicillian.json', 'users.json']    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)        

    @classmethod 
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()
    
    def test_login(self):
        timeout = 5        
        
        login_user(self.driver, timeout -3, self.live_server_url)

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text()="Menu"]'))
        )        

        
        sub = self.driver.find_element(By.XPATH, "//h2[@id='headingTwo']")
        pasta = self.driver.find_element(By.XPATH, "//h2[@id='headingThree']")
        salad = self.driver.find_element(By.XPATH, "//h2[@id='headingFour']")
        platter = self.driver.find_element(By.XPATH, "//h2[@id='headingFive']")

        actions = ActionChains(self.driver, 5)

        scroll_to_menu_button(actions, self.driver, sub)        
        scroll_to_menu_button(actions, self.driver, pasta)
        scroll_to_menu_button(actions, self.driver, salad)
        scroll_to_menu_button(actions, self.driver, platter)                
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        self.assertIn('Regular', self.driver.page_source)
        self.assertIn('Sicillian', self.driver.page_source)
        self.assertIn('Pasta', self.driver.page_source)
        self.assertIn('Salad', self.driver.page_source)
        self.assertIn('Platter', self.driver.page_source)
        self.assertIn('Sub', self.driver.page_source)        
        self.assertIn('Small', self.driver.page_source)
        self.assertIn('Large', self.driver.page_source)
        self.assertIn('Profile', self.driver.page_source)
        self.assertIn('Special', self.driver.page_source)
        self.assertIn('Cheese', self.driver.page_source)
        self.assertIn('+ Mushrooms', self.driver.page_source)
        self.assertIn('Special', self.driver.page_source)
        self.assertIn('Canadian Bacon', self.driver.page_source)
        self.assertIn('Chicken Parm', self.driver.page_source)

    def test_profile(self):
        timeout = 5


        login_user(self.driver, timeout -3, self.live_server_url)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="dropdownMenuButton1"]'))
        )   
        self.assertNotIn('Username', self.driver.page_source)
        self.assertIn('TestUser', self.driver.page_source)
        dropdown_button = self.driver.find_element(By.XPATH, '//button[@id="dropdownMenuButton1"]')
        dropdown_button.click()

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dropdown-menu'))
        )   
        profile_button = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu li')[0]
        profile_button.click()

        time.sleep(4)
        self.assertIn('TestUser', self.driver.page_source)
        self.assertIn('Test User', self.driver.page_source)
        self.assertIn('test@gmail.com', self.driver.page_source)
        self.assertIn('Update Profile', self.driver.page_source)
        time.sleep(3)

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Update Profile'))
        )   
        update_profile_button = self.driver.find_element(By.LINK_TEXT, 'Update Profile')
        update_profile_button.click()

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//form[@id="update-profile-form"]'))
        )   

        name_input = self.driver.find_element(By.CSS_SELECTOR, '#id_name')
        username_input = self.driver.find_element(By.CSS_SELECTOR, '#id_username')
        email_input = self.driver.find_element(By.CSS_SELECTOR, '#id_email')

        name_input.clear()
        name_input.send_keys('Test Updated User')
        username_input.clear()
        username_input.send_keys('TestUpdatedUser')
        email_input.clear()
        email_input.send_keys('testupdated@gmail.com')
        time.sleep(4)

        email_input.send_keys(Keys.ENTER)

        time.sleep(4)

        self.assertIn('Test Updated User', self.driver.page_source)
        self.assertIn('TestUpdatedUser', self.driver.page_source)
        self.assertIn('testupdated@gmail.com', self.driver.page_source)



        time.sleep(4)

    def test_login_logout(self):
        timeout = 5        
        
        login_user(self.driver, timeout -3, self.live_server_url)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="dropdownMenuButton1"]'))
        )   
        self.assertNotIn('Username', self.driver.page_source)
        self.assertIn('TestUser', self.driver.page_source)
        dropdown_button = self.driver.find_element(By.XPATH, '//button[@id="dropdownMenuButton1"]')
        dropdown_button.click()

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dropdown-menu'))
        )   
        logout_button = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu li')[1]
        logout_button.click()

        time.sleep(4)
        self.assertNotIn('TestUser', self.driver.page_source)
        self.assertIn('Username', self.driver.page_source)

        dropdown_button = self.driver.find_element(By.XPATH, '//button[@id="dropdownMenuButton1"]')
        dropdown_button.click()
        time.sleep(4)
        login_button = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu li')[0]
        login_button.click()

        time.sleep(3)

        login_user(self.driver, timeout -3, self.live_server_url)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="dropdownMenuButton1"]'))
        )   
        self.assertNotIn('Username', self.driver.page_source)
        self.assertIn('TestUser', self.driver.page_source)

    def test_register(self):
        timeout = 5

        self.driver.get('%s%s'%(self.live_server_url, '/user/login/'))
        time.sleep(4)

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'here'))
        )   
        register_user_button = self.driver.find_element(By.LINK_TEXT, 'here')
        register_user_button.click()

        time.sleep(3)

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//form[@id="register-user-form"]'))
        )   

        name_input = self.driver.find_element(By.CSS_SELECTOR, '#id_name')
        username_input = self.driver.find_element(By.CSS_SELECTOR, '#id_username')
        email_input = self.driver.find_element(By.CSS_SELECTOR, '#id_email')
        password1_input = self.driver.find_element(By.CSS_SELECTOR, '#id_password1')
        password2_input = self.driver.find_element(By.CSS_SELECTOR, '#id_password2')

        name_input.send_keys('Test User Two')
        time.sleep(2)
        username_input.send_keys('TestUserTwo')
        time.sleep(2)
        email_input.send_keys('testusertwo@mail.com')
        time.sleep(2)
        password1_input.send_keys('Test User Two')
        time.sleep(2)
        password2_input.send_keys('Test User Two')
        time.sleep(2)
        password2_input.send_keys(Keys.ENTER)

        self.assertIn("too similar", self.driver.page_source)

        time.sleep(2)
        password1_input = self.driver.find_element(By.CSS_SELECTOR, '#id_password1')
        password2_input = self.driver.find_element(By.CSS_SELECTOR, '#id_password2')
        password1_input.send_keys('u555me666$!(')
        time.sleep(2)
        password2_input.send_keys('u555me666$!(')
        time.sleep(2)
        password2_input.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text()="Menu"]'))
        )        

        
        self.assertIn('TestUserTwo', self.driver.page_source)

        dropdown_button = self.driver.find_element(By.XPATH, '//button[@id="dropdownMenuButton1"]')
        dropdown_button.click()

        time.sleep(2)

        profile_button = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu li')[0]
        profile_button.click()

        time.sleep(4)
        self.assertIn('TestUserTwo', self.driver.page_source)
        self.assertIn('Test User Two', self.driver.page_source)
        self.assertIn('testusertwo@mail.com', self.driver.page_source)
        self.assertIn('Update Profile', self.driver.page_source)
        time.sleep(3)
        