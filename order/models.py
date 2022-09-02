from django.db import models
from base.models import User
from django.contrib.humanize.templatetags import humanize

# Create your models here.

STATUS_CHOICES = (
    ('PLACED', 'placed'),
    ('COOKING', 'cooking'),
    ('DELIVERING', 'delivering'),
    ('DELIVERED', 'delivered'),
)

class OrderedItem(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    food_item = models.CharField(max_length=64, null=True, blank=False)
    choices = models.CharField(max_length=64, null=True, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=False, default='PLACED')
    created = models.DateTimeField(auto_now_add=True)

    # @property 
    # def timeordered(self):
    #     return timesince.timesince(self.created)
    @property
    def get_time(self):
        return humanize.naturaltime(self.created)



