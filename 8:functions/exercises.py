# # Exercise 8.1
# def display_message(message):
#   print(message)

# display_message("Im learning about functions")

# # Exercise 8.2
# def favorite_book(book):
#   print(f"One of my favorite books is {book}")

# favorite_book("Dune")

# # Exercise 8.3 - 8.4
# def make_shirt(size="large", text="I love python"):
#   print(f"Im making a shirt of size: {size} " 
#         f"and the message it has printed is {text}")
  
# make_shirt()
# make_shirt("large", "sampĺe text")
# make_shirt(text="another text", size="medium")

# # Exercise 8.5
# def describe_city(name, country="Portugal"):
#   print(f"{name} is in {country}")

# describe_city("Lisboa")
# describe_city("Reykjavik", "Iceland")
# describe_city("Aarhus", "Denmark")

# # Exercise 8.6
# def city_country(city, country):
#   return f"{city}, {country}"

# print(city_country("Santiago", "Chile"))

# # Exercise 8.7-8.8
# def make_album(artist, album, tracks=''):
#   baseInfo = {
#     "artist": artist,
#     "album": album,
#   }
#   if tracks:
#     baseInfo["tracks"] = tracks
#   return baseInfo

# # print(make_album("Frank Ocean", "Blond"))
# # print(make_album("Tame Impala", "Currents", 12))

# while(True):
#   new_album = input("Press enter to add a new album ")
#   new_artist = input("Whats the artist name? ")
#   print(make_album(new_album, new_artist))
#   break

# # Exercise 8.9-8.10
# magicians_list = ["David Copperfield", "David Blaine", "Criss Angel"]

# def show_magicians(array):
#   for magician in array:
#     print(magician)

# def make_great(array):
#   for i in range(len(array)):
#     array[i] = f"The great {array[i]}"

# show_magicians(magicians_list)

# # Exercise 8.11
# magicians_copy = magicians_list[:]

# make_great(magicians_copy)
# print('This is a copy: ', magicians_copy)

# # Exercise 8.12
# sandwich_toppings = ["ham", "cheese", "lettuce"]

# def sandwich_summary(topping_list):
#   print("Your sandwich will have: ")
#   for topping in topping_list:
#     print(topping)

# sandwich_summary(sandwich_toppings)

# Exercise 8.13
def build_profile(first, last, age, city, hobbies):
  full_name = first + " " + last
  return {
    "full_name": full_name,
    "age": age,
    "city": city,
    "hobbies": hobbies 
  }

print(build_profile("John", "Doe", 30, "Lisbon", ["reading", "coding"]))

# Exercise 8.14
def make_car(manufacturer, model, **specs): # It accepts an arbitrary number of keyword arguments
  car = {
    "manufacturer": manufacturer,
    "model": model
  }
  if (specs):
    for key, value in specs.items():
      car[key] = value
  print(car)
  return car

car = make_car('subaru', 'outback', color='blue', tow_package=True)
