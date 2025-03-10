import unittest
from employees import Employees

#Exercise 3
class test_employees(unittest.TestCase):
  """ Tests for the class Employees """
  def setUp(self):
    self.employee = Employees('Steve', 'Jobs', 100000)

  def test_give_default_raise(self):
    self.employee.give_raise()
    result = self.employee.annual_salary
    self.assertEqual(result, 105000)

  def test_give_custom_raise(self):
    self.employee.give_raise(20000)
    result = self.employee.annual_salary
    self.assertEqual(result, 120000)

unittest.main()