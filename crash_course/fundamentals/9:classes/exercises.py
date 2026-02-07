# Exercise 9.13
from collections import OrderedDict

# from 6.3-6.4
glossary = OrderedDict()

glossary = {
    'list': 'A collection of items in a particular order.',
    'tuple': 'A collection of items that cannot change.',
    'dictionary': 'A collection of key-value pairs.',
    'string': 'A series of characters.',
    'integer': 'A whole number.',
}

glossary['set'] = 'A collection of unique items.'
glossary['if'] = 'A conditional statement.'
glossary['append'] = 'A method that adds an item to a list.'

for value, key in glossary.items():
  print(f" A {value} is {key}")

# Exercise 9.14
from random import randint

class Dice():
  def __init__(self, sides):
    self.sides = sides
  
  def roll_dice(self):
    return randint(1, self.sides)
  
six_sided_dice = Dice(6)
print(six_sided_dice.roll_dice())

ten_sided_dice = Dice(10)
twenty_sided_dice = Dice(20)

for i in range(0, 10):
  print("10: ", ten_sided_dice.roll_dice())
  print("20: ", twenty_sided_dice.roll_dice())
