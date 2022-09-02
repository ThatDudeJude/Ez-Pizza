from django.test import TestCase, Client
from django.core.management import call_command
from base.models import User

# class 

class UserAuthenticationPageTestCase(TestCase):    


    def test_login_page(self):
        c = Client()

        response = c.get("/user/login/")
        self.assertEqual(200, response.status_code)
        self.assertIn(b'Login', response.content)
        self.assertIn(b"Don't have an account", response.content)
        self.assertIn(b'Username', response.content)
        self.assertIn(b'Password', response.content)
        self.assertIn(b'Register', response.content)

    def test_register_page(self):
        c = Client()

        response = c.get("/user/register/")        
        self.assertEqual(200, response.status_code)
        self.assertIn(b'Username', response.content)
        self.assertIn(b'Email', response.content)
        self.assertIn(b'Password', response.content)
        self.assertIn(b'Confirm', response.content)
        self.assertIn(b'Login', response.content)

    def test_register_user(self):
        # c = Client()        
        # c.get('/user/register/')
        call_command('fooditems', ['-a'])

        response = self.client.post('/user/register/', {
            'name': 'Test User',
            'username': 'TestUser',
            'email': 'test@gmail.com',
            'password1': 'pbkdf2_sha256$260000$cVQj9JKZakfB9MZOIABtLR$aUVWcy04MUw8eLUxdBEBNXjKL+20PJ9fMq31H0sHeag=',
            'password2': 'pbkdf2_sha256$260000$cVQj9JKZakfB9MZOIABtLR$aUVWcy04MUw8eLUxdBEBNXjKL+20PJ9fMq31H0sHeag=',
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestUser', response.content)
        self.assertIn(b'Menu', response.content)
        


class UserAuthenticationTestCase(TestCase):
    fixtures = ['users.json']

    def test_user_exists(self):
        user = User.objects.filter(email="test@gmail.com")        
        self.assertTrue(user.exists())

    def test_user_login(self):
        user = User.objects.get(email="test@gmail.com")        
        
        c = Client()

        # authenticated = c.login(email=user.email, password='u555me666$!(')        
        
        # self.assertTrue(authenticated)

        response = c.post("/user/login/", {
            "email": user.email,
            "password": "u555me666$!("
        }, 
        follow=True)
        self.assertIn('base/index.html',response.templates[0].name)
        self.assertEqual(response.status_code, 200)        
        self.assertIn(b'TestUser', response.content)
        self.assertIn(b'Menu', response.content)              
        self.assertIn(b'Small', response.content)
        self.assertIn(b'Large', response.content)
        self.assertIn(b'Profile', response.content)


    def test_login_required_redirect(self):

        c = Client()
        response  = c.get('/shop/view-cart/page/', follow=True)

        self.assertIn('base/login_register.html', response.templates[0].name)
                
    
    def test_login_logout(self):
        user = User.objects.get(username='TestUser')
        c = Client()
        response = c.post('/user/login/', {
            'email': user.email,
            'password': 'u555me666$!('
        }, follow=True)

        self.assertIn('base/index.html',response.templates[0].name)
        self.assertEqual(response.status_code, 200)        
        self.assertIn(b'TestUser', response.content)                
        self.assertIn(b'Profile', response.content)
        self.assertIn(b'Logout', response.content)

        response = c.get('/user/logout/', follow=True)

        self.assertIn('base/index.html',response.templates[0].name)
        self.assertEqual(response.status_code, 200)        
        self.assertIn(b'Username', response.content)                
        self.assertIn(b'Login', response.content)

class ProfileTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        user = User.objects.get(email='test@gmail.com')
        self.client.login(email=user.email, password='u555me666$!(')

    def test_view_user_profile(self):
        response = self.client.get('/user/profile/view/')

        self.assertIn(b'test@gmail.com', response.content)
        self.assertIn(b'default_avatar.svg', response.content)
        self.assertIn(b'Update Profile', response.content)

    def test_update_user_profile(self):
        response = self.client.post('/user/profile/update/', {
        #    'avatar': 'default_avatar.svg', 
           'name': 'Updated Test User', 
           'username': 'TestUserUpdated',
           'email': 'testupdated@gmail.com'
        }, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertIn(b"Updated Test User", response.content)
        self.assertIn(b"TestUserUpdated", response.content)
        self.assertIn(b"testupdated@gmail.com", response.content)
        self.assertNotIn(b"test@gmail.com", response.content)        
    