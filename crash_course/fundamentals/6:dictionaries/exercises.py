# 6.1 
person = {
    'first_name': 'John',
    'last_name': 'Doe',
    'age': 30,
    'city': 'New York',
}

# 6.2
favorite_numbers = {
    'John': 7,
    'Jane': 3,
    'Alice': 9,
    'Bob': 2,
    'Eve': 1,
}

# 6.3-6.4
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

# 6.5
rivers = {
    'nile': 'egypt',
    'amazon': 'brazil',
    'yangtze': 'china',
}

for river, country in rivers.items():
    print(f"The {river.title()} runs through {country.title()}.")

for river in rivers: 
   print(river.title())

for river in rivers.values():
  print(river.title())

#6.6
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

people = ['jen', 'sarah', 'edward', 'phil', 'john', 'jane']

for person in people:
    if person not in favorite_languages.keys():
        print(f"{person.title()}, please take our poll.")
    else: 
        print(f"{person.title()}, thank you for responding to the poll.")

#6.7
person1 = {
    'first_name': 'John',
    'last_name': 'Doe',
    'age': 30,
    'city': 'New York',
}

person2 = {
    'first_name': 'Jane',
    'last_name': 'Doe',
    'age': 25,
    'city': 'Los Angeles',
}

person3 = {
    'first_name': 'Jim',
    'last_name': 'Beam',
    'age': 50,
    'city': 'New York',
}

people = [person1, person2, person3]

for person in people: 
   print(f"Hi my name is {person['first_name']} {person['last_name']}, "
        f"im {person['age']} years old and i live in {person['city']}")

#6.8 
pet1 = {
    'name': 'Buddy',
    'animal': 'dog',
    'owner': 'John',
}

pet2 = {
    'name': 'Whiskers',
    'animal': 'cat',
    'owner': 'Jane',
}

pet3 = {
    'name': 'Fido',
    'animal': 'dog',
    'owner': 'Jim',
}

pets = [pet1, pet2, pet3]

for pet in pets: 
    print(f"Im {pet['owner']} and my {pet['animal']}´s name is {pet['name']}")

#6.9
favorite_places = {
    'John': ['New York', 'Los Angeles', 'Chicago'],
    'Jane': ['Los Angeles', 'San Francisco', 'Chicago'],
    'Jim': ['New York', 'Chicago', 'San Francisco'],
}

for person in favorite_places:
    print(f"{person} favorite places are:")
    for place in favorite_places[person]:
        print(f"- {place}")

#6.10
favorite_numbers = {
    'John': [7, 3, 9],
    'Jane': [3, 1, 2],
    'Jim': [2, 4, 6],
}

for person in favorite_numbers:
   print(f"{person} favorite numbers are:")
   for number in favorite_numbers[person]:
      print(f"- {number}")

#6.11-6.12
cities = {
    'New York': {
        'country': 'United States',
        'population': 8400000,
        'fact': 'The city that never sleeps.'
    },
    'Los Angeles': {
        'country': 'United States',
        'population': 3900000,
        'fact': 'The city of angels.'
    },
    'Chicago': {
        'country': 'United States',
        'population': 2700000,
        'fact': 'The city of big shoulders.'
    },
}

for city in cities:
   print(f"Some info about {city}: ")
   for key, value in cities[city].items():
      print(f"{key}: {value}")




    