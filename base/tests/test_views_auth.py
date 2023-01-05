from django.test import TestCase, Client
from django.core.management import call_command
from base.models import User
from django.urls import reverse
from django.core import mail
import sys

# class


class UserAuthenticationPageTestCase(TestCase):
    def test_login_page(self):
        c = Client()

        response = c.get("/user/login/")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Login", response.content)
        self.assertIn(b"Don't have an account", response.content)
        self.assertIn(b"Email", response.content)
        self.assertIn(b"Password", response.content)
        self.assertIn(b"Register", response.content)

    def test_register_page(self):
        c = Client()

        response = c.get("/user/register/")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Username", response.content)
        self.assertIn(b"Email", response.content)
        self.assertIn(b"Password", response.content)
        self.assertIn(b"Confirm", response.content)
        self.assertIn(b"Login", response.content)

    def test_register_user(self):
        # c = Client()
        # c.get('/user/register/')
        call_command("fooditems", ["-a"])

        response = self.client.post(
            "/user/register/",
            {
                "name": "Test User",
                "username": "TestUser",
                "email": "test@gmail.com",
                "password1": "123!@#QWE",
                "password2": "123!@#QWE",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TestUser", response.content)
        self.assertIn(b"Menu", response.content)

        with open("fixtures/testuser.json", "w") as f:
            call_command("dumpdata", "base.user", stdout=f)


class UserAuthenticationTestCase(TestCase):
    fixtures = ["testuser.json"]

    def test_user_exists(self):
        user = User.objects.filter(email="test@gmail.com")
        self.assertTrue(user.exists())

    def test_user_login(self):
        user = User.objects.get(email="test@gmail.com")

        c = Client()

        # authenticated = c.login(email=user.email, password='123!@#QWE')

        # self.assertTrue(authenticated)

        response = c.post(
            "/user/login/", {"email": user.email, "password": "123!@#QWE"}, follow=True
        )
        self.assertIn("base/index.html", response.templates[0].name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TestUser", response.content)
        self.assertIn(b"Menu", response.content)
        self.assertIn(b"Small", response.content)
        self.assertIn(b"Large", response.content)
        self.assertIn(b"Profile", response.content)

    def test_login_required_redirect(self):

        c = Client()
        response = c.get("/shop/view-cart/page/", follow=True)

        self.assertIn("base/login_register.html", response.templates[0].name)

    def test_login_logout(self):
        user = User.objects.get(username="TestUser")
        c = Client()
        response = c.post(
            "/user/login/", {"email": user.email, "password": "123!@#QWE"}, follow=True
        )

        self.assertIn("base/index.html", response.templates[0].name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TestUser", response.content)
        self.assertIn(b"Profile", response.content)
        self.assertIn(b"Logout", response.content)

        response = c.get("/user/logout/", follow=True)

        self.assertIn("base/index.html", response.templates[0].name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username", response.content)
        self.assertIn(b"Login", response.content)


class ProfileTestCase(TestCase):
    fixtures = ["testuser.json"]

    def setUp(self):
        user = User.objects.get(email="test@gmail.com")
        self.client.login(email=user.email, password="123!@#QWE")

    def test_view_user_profile(self):
        response = self.client.get("/user/profile/view/")

        self.assertIn(b"test@gmail.com", response.content)
        self.assertIn(b"default_avatar.jpg", response.content)
        self.assertIn(b"Update Profile", response.content)

    def test_update_user_profile(self):
        response = self.client.post(
            "/user/profile/update/",
            {
                #    'avatar': 'default_avatar.jpg',
                "name": "Updated Test User",
                "username": "TestUserUpdated",
                "email": "testupdated@gmail.com",
            },
            follow=True,
        )

        self.assertEqual(200, response.status_code)
        self.assertIn(b"Updated Test User", response.content)
        self.assertIn(b"TestUserUpdated", response.content)
        self.assertIn(b"testupdated@gmail.com", response.content)
        self.assertNotIn(b"test@gmail.com", response.content)


class PasswordChangeTestCase(TestCase):
    fixtures = ["testuser.json"]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(email="test@gmail.com")

    def test_view_password_change(self):
        c = Client()
        c.post(
            "/user/login/",
            {"email": self.user.email, "password": "123!@#QWE"},
            follow=True,
        )
        response = c.post(
            reverse("user-password-change"),
            {
                "old_password": "123!@#QWE",
                "new_password1": "456!@#QWE",
                "new_password2": "456!@#QWE",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/password_change_done.html")
        response = c.post(
            "/user/login/",
            {"email": self.user.email, "password": "456!@#QWE"},
            follow=True,
        )

        self.assertTemplateUsed(response, "base/index.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestUser")
        self.assertContains(response, "Profile")
        self.assertContains(response, "Logout")


class PasswordResetTestCase(TestCase):
    fixtures = ["testuser.json"]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(email="test@gmail.com")

    def test_view_password_reset_page(self):
        c = Client()
        response = c.get(reverse("password-reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/password_reset_form.html")

    def test_view_password_reset_send_email(self):
        c = Client()
        response = c.post(reverse("password-reset"), {"email": "test@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/password_reset_done.html")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Reset your ezPizza account password")
        self.assertIn("Test User", mail.outbox[0].body)
        

    def test_view_password_reset_via_email(self):
        c = Client()
        response = c.post(reverse("password-reset"), {"email": "test@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/password_reset_done.html")
        token = response.context[0]["token"]
        uid = response.context[0]["uid"]
        response = c.get(
            reverse("confirm-password-reset", kwargs={"uidb64": uid, "token": token})
        )
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "base/password_reset_confirm.html")

        response = c.post(
            reverse("confirm-password-reset", kwargs={"uidb64": uid, "token": token}),
            {"new_password1": "456!@#QWE", "new_password2": "456!@#QWE"},
        )

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "base/password_change_done.html")

        response = c.post(
            "/user/login/",
            {"email": self.user.email, "password": "456!@#QWE"},
            follow=True,
        )

        self.assertTemplateUsed(response, "base/index.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestUser")
        self.assertContains(response, "Profile")
        self.assertContains(response, "Logout")
