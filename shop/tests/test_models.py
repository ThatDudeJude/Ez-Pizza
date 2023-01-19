from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch
from django.conf import settings
from io import StringIO
import os
import csv

from shop.models import Regular, Sicillian, Topping, Sub, Pasta, Salad, Platter


class CustomCommandTestCase(TestCase):
    def test_add_items_command(self):
        out = StringIO()
        args = ["--add"]

        call_command("fooditems", args, stdout=out)

        self.assertIn("Food items successfully added", out.getvalue())

    def test_food_items_already_added(self):
        out = StringIO()
        args = ["-a"]

        call_command("fooditems", args)

        call_command("fooditems", args, stdout=out)

        self.assertIn("Food items already added", out.getvalue())

    @patch("base.management.commands.fooditems.input")
    def __input_call__delete_wrapper(self, input_response_value, mock_input=None):
        def input_response(message):
            return input_response_value

        mock_input.side_effect = input_response
        out = StringIO()
        args = ["-del"]
        call_command("fooditems", args, stdout=out)
        return out.getvalue()

    def test_add_items_something_went_wrong(self):

        args = ["-a"]

        call_command("fooditems", args)

        self.assertIn(
            "Successfully deleted all food items data",
            self.__input_call__delete_wrapper("y"),
        )
        # self.assertEqual(1, 1)


class RegularDataTestCase(TestCase):
    fixtures = ["regular.json", "regular"]

    def test_regular_pizza_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "regular_pizza.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            index = 1
            for row in reader:
                regular = Regular.objects.get(pk=index)
                self.assertEqual(regular.delicacy, row[0])
                self.assertEqual(str(regular.small), row[1])
                self.assertEqual(str(regular.large), row[2])
                index += 1


class SicillianDataTestCase(TestCase):
    fixtures = ["sicillian.json", "sicillian"]

    def test_sicillian_pizza_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "sicillian_pizza.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            index = 1
            for row in reader:
                sicillian = Sicillian.objects.get(pk=index)
                self.assertEqual(sicillian.delicacy, row[0])
                self.assertEqual(str(sicillian.small), row[1])
                self.assertEqual(str(sicillian.large), row[2])
                index += 1


class ToppingDataTestCase(TestCase):
    fixtures = ["topping.json", "topping"]

    def test_topping_pizza_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "toppings.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            index = 1
            for row in reader:
                topping = Topping.objects.get(pk=index)
                self.assertEqual(topping.topping, row[0])
                index += 1


class SubDataTestCase(TestCase):
    fixtures = ["sub.json", "sub"]

    def test_sub_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "subs.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            next(reader)
            index = 1
            for row in reader:
                sub = Sub.objects.get(pk=index)
                self.assertEqual(sub.sub, row[0])
                self.assertIn(str(sub.small), row[1])
                self.assertIn(str(sub.large), row[2])
                index += 1


class PastaDataTestCase(TestCase):
    fixtures = ["pasta.json", "pasta"]

    def test_pasta_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "pasta.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            index = 1
            for row in reader:
                pasta = Pasta.objects.get(pk=index)
                self.assertEqual(pasta.pasta, row[0])
                self.assertEqual(str(pasta.fixed), row[1])
                index += 1


class SaladDataTestCase(TestCase):
    fixtures = ["salad.json", "salad"]

    def test_salad_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "salads.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            index = 1
            for row in reader:
                salad = Salad.objects.get(pk=index)
                self.assertEqual(salad.salad, row[0])
                self.assertEqual(str(salad.fixed), row[1])
                index += 1


class PlatterDataTestCase(TestCase):
    fixtures = ["platter.json", "platter"]

    def test_platter_model(self):

        with open(
            os.path.join(settings.BASE_DIR, "csv_files", "platters.csv"), "r"
        ) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            index = 1
            for row in reader:
                platter = Platter.objects.get(pk=index)
                self.assertEqual(platter.platter, row[0])
                self.assertEqual(str(platter.small), row[1])
                self.assertEqual(str(platter.large), row[2])
                index += 1
