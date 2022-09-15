# Generated by Django 3.2.13 on 2022-09-15 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_item', models.CharField(max_length=64, null=True)),
                ('choices', models.CharField(max_length=64, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('status', models.CharField(choices=[('PLACED', 'placed'), ('COOKING', 'cooking'), ('DELIVERING', 'delivering'), ('DELIVERED', 'delivered')], default='PLACED', max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
