# Exercise 5.1 
cars = ['Audi', 'Bmw', 'Subaru', 'Toyota']
print("Is car == 'Subaru'? I predict True.")
print(cars[2] == 'Subaru')

print("\nIs car == 'audi'? I predict False.")
print(cars[1].lower() == 'audi')

# Exercise 5.2
print("\nIs cars[0] == 'audi' or cars[0] == 'Bmw'? I predict True.")
print(cars[0] == 'audi' or cars[0] == 'Bmw')

print("\nIs 'Ferrari' in cars? I predict False.")
print('Ferrari' in cars)

print("\nIs Lamborghini not in cars? I predict True.")
print('Lamborghini' not in cars)

print("\nIs the length of cars 4? I predict True.")
print(len(cars) == 4 and len(cars) < 5 and len(cars) > 3)

#5.3-5.5
alien_color = 'green'
if alien_color == 'green':
    print("You just earned 5 points!")
elif alien_color == 'yellow':
    print("You just earned 10 points!")
else:
    print("You just earned 15 points!")

#5.6
age = 20
if age < 2:
    print("You are a baby.")
elif age >= 2 and age < 4:
    print("You are a toddler.")
elif age >= 4 and age < 13:
    print("You are a kid.")
elif age >= 13 and age < 20:
    print("You are a teenager.")
elif age >= 20 and age < 65:
    print("You are an adult.")
else:
    print("You are an elder.")

#5.7
favorite_fruits = ['apple', 'banana', 'orange']
if 'apple' in favorite_fruits:
    print("You really like apples!")

#5.8-5.9
users = ['admin', 'user1', 'user2', 'user3', 'user4']
# users = []

if users: 
  for user in users:
      if user == 'admin':
          print("Hello admin, would you like to see a status report?")
      else:
          print("Hello " + user + ", thank you for logging in again.")
else:
    print("We need to find some users!")

#5.10
current_users = ['admin', 'user1', 'user2', 'user3', 'user4']
new_users = ['user1', 'User5', 'USER6', 'user7', 'USER2']

for new_user in new_users:
    if new_user.lower() in current_users:
        print("Sorry, the username " + new_user + " is already taken.")

#5.11
numbers = list(range(1, 10))
for number in numbers:
    if number == 1:
        print(str(number) + "st")
    elif number == 2:
        print(str(number) + "nd")
    elif number == 3:
        print(str(number) + "rd")
    else:
        print(str(number) + "th")

