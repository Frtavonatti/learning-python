## Exercise 4.1
pizzas = ['pepperoni', 'margherita', 'capricciosa']
for pizza in pizzas:
    print(f"I like {pizza} pizza.")
print("I really love pizza!")

## Exercise 4.2
animals = ['dog', 'cat', 'rabbit']
for animal in animals:
    print(f"A {animal} would make a great pet.")
print("Any of these animals would make a great pet!")

## Exercise 4.3
for value in range(1, 21):
    print(value)

## Exercise 4.4
for value in range(1, 1000001):
    print(value)

# Exercise 4.5
millionList = range(1, 1000001)
print('Max: ', min(millionList))
print('Min: ', max(millionList))
print('Sum: ', sum(millionList))

## Exercise 4.6
oddNumbers = range(1, 21, 2)
for number in oddNumbers:
    print(number)

evenNumbers = range(2, 21, 2)
for number in evenNumbers:
    print(number)

## Exercise 4.7
multiplesOfThree = range(3, 31, 3)
for number in multiplesOfThree:
    print(number)

## Exercise 4.8
for number in range(1, 11):
    print(number**3)

## Exercise 4.9
cubes = [number**3 for number in range(1, 11)]
print(cubes)

## Exercise 4.10
cubes = [number**3 for number in range(1, 11)]
print(f'The first three numbers in the list are {cubes[0:3]}')
print(f'The four numbers from the middle of the list are {cubes[3:7]}')
print(f'The last three numbers in the list are {cubes[7:11]}')

## Exercise 4.11
pizzas = ['pepperoni', 'margherita', 'capricciosa']
copyOfPizzas = pizzas[:]

pizzas.append('carbonara')
copyOfPizzas.append('napolitana')

for pizza in pizzas:
    print('Original array: ', pizza)

for pizza in copyOfPizzas:
    print('New Array: ', pizza)

## Exercise 4.13
foods = ('pizza', 'pasta', 'salad', 'soup', 'burger')
for food in foods:
    print(food)

# foods[0] = 'fries'  This will throw an error because tuples are immutable

foods = ('fries', 'pasta', 'sandwich', 'soup', 'burger')
for food in foods:
    print(food)

    
