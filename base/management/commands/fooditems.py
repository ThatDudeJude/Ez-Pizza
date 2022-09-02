from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError
# from django.utils.six.moves import input
from shop.models import Regular, Sicillian, Topping, Sub, Pasta, Salad, Platter, SpecialRegular, SpecialSicillian
import csv
import os

class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument(
            '-a', '--add',
            action='store_true',
            help='Add data to database'
        )

        parser.add_argument(
            '-del','--delete',
            action='store_true',
            help = 'Delete data from database'

        )

    def handle(self, *args, **options):        
        
        if options['add']:
            try:

                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'regular_pizza.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader: 
                        item = Regular.objects.create(delicacy=row[0], small=float(row[1]), large=float(row[2]))
                        item.save()
                        
                
                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'sicillian_pizza.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader: 
                        item = Sicillian.objects.create(delicacy=row[0], small=float(row[1]), large=float(row[2]))
                        item.save()

                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'toppings.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader: 
                        item = Topping.objects.create(topping=row[0])
                        item.save()

                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'subs.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file, delimiter=";")
                    next(reader)

                    for row in reader: 
                        item = Sub.objects.create(sub=row[0], small=float(row[1]), large=float(row[2]))
                        item.save()


                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'pasta.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader: 
                        item = Pasta.objects.create(pasta=row[0], fixed=float(row[1]))
                        item.save()

                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'salads.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader: 
                        item = Salad.objects.create(salad=row[0], fixed=float(row[1]))
                        item.save()

                with open(os.path.join(settings.BASE_DIR, 'csv_files', 'platters.csv'), 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader: 
                        item = Platter.objects.create(platter=row[0], small=float(row[1]), large=float(row[2]))                
                        item.save()
                
                item = SpecialRegular.objects.create(delicacy='Sausage | Pineapple | Green Peppers | Anchovies', small=18.50, large=26.95)
                item.save()

                item = SpecialSicillian.objects.create(delicacy='Sausage | Pineapple | Green Peppers | Anchovies', small=33.50, large=47.95)
                item.save()

                self.stdout.write(self.style.SUCCESS("Food items successfully added."))
            except IntegrityError:
                self.stdout.write(self.style.ERROR("Food items already added."))
            except:
                self.stdout.write(self.style.ERROR("Something went wrong."))

        if options['delete']:

            result = input("Delete all food items? [Y/N]: ")

            if result.lower() == 'y':

                Regular.objects.all().delete()
                Sicillian.objects.all().delete()
                Topping.objects.all().delete()
                Sub.objects.all().delete()
                Pasta.objects.all().delete()
                Salad.objects.all().delete()
                Platter.objects.all().delete()
                SpecialSicillian.objects.all().delete()
                SpecialRegular.objects.all().delete()
                self.stdout.write(self.style.SUCCESS("Successfully deleted all food items data."))
            else:
                self.stdout.write(self.style.SUCCESS("Exiting...."))
