import unittest
from recipe import parse


class TestRecipe(unittest.TestCase):
    def test_parse_carrot(self):
        recipes = parse(open('pages/carrot.html'))
<<<<<<< HEAD
        self.assertIsInstance(recipes, list, "The `parse` method should return a `list`")
        self.assertIsInstance(recipes[0], dict, "The `parse_recipe` method should return a `list` of `dict` objects")
=======
        self.assertIsInstance(recipes, list, "The `parse` method should return a `list` of `dict` objects")
        self.assertIsInstance(recipes[0], dict, "The `parse_recipe` method should return a `dict` object")
>>>>>>> master
        self.assertEqual(recipes[0]['name'], 'Beef Carrot Stew')
        self.assertEqual(recipes[0]['difficulty'], 'Very easy')
        self.assertEqual(recipes[0]['prep_time'], '45 min')
