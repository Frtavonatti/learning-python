import unittest
from city_functions import describe_city

# Exercises 1-2
class TestCityFunction(unittest.TestCase):
  """ Tests for city_functions """
  def test_city_and_country(self):
    city = describe_city('Santiago', 'Chile')
    self.assertEqual(city, 'Santiago, Chile')
  
  def test_city_country_population(self):
    result = describe_city('Santiago', 'Chile', 5000000)
    self.assertEqual(result, 'Santiago, Chile - population: 5000000')

unittest.main()
