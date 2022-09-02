from django.db import models
from base.models import User

# Create your models here.

class Regular(models.Model):
    small_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='small', max_length=4)
    large_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='large', max_length=4)
    delicacy = models.CharField(max_length=64, null=True, unique=True)

class Sicillian(models.Model):
    small_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='small')
    large_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='large')
    delicacy = models.CharField(max_length=64, null=True, unique=True)

class Topping(models.Model):
    name = models.CharField(max_length=64, name='topping', unique=True)
    
    def __str__(self):
        return f"{self.topping}"

class Sub(models.Model):
    name = models.CharField(max_length=64, name='sub', unique=True)
    small_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='small')
    large_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='large')

class Pasta(models.Model):
    name = models.CharField(max_length=64, name='pasta', unique=True)
    fixed_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='fixed')

class Salad(models.Model):
    name = models.CharField(max_length=64, name='salad', unique=True)
    fixed_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='fixed')

class Platter(models.Model):
    name = models.CharField(max_length=64, name='platter', unique=True)
    small_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='small')
    large_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='large')

class SpecialRegular(models.Model):
    small_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='small', max_length=4)
    large_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='large', max_length=4)
    delicacy = models.CharField(max_length=64, null=True)

class SpecialSicillian(models.Model):
    small_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='small', max_length=4)
    large_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, name='large', max_length=4)
    delicacy = models.CharField(max_length=64, null=True)

class ShoppingCartItem(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    food_item = models.CharField(max_length=64, null=True, blank=False)
    choices = models.CharField(max_length=64, null=True, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)