# Exercises 2.3-2.7
name = "  Eric  "

name = name.strip()

title_name = name.title()
lower_name = name.lower()
upper_name = name.upper()

message = (f"Hello: \n{title_name} \n{upper_name} \n{lower_name}  !");
# print(message)


# Exercises 3.4-3.7
guests = ['Albert Einstein', 'Isaac Newton', 'Nikola Tesla']

# for guest in guests:
#   print(f"Hello {guest}, would you like to have dinner with me?")

## Exercise 3.5
guests.remove('Albert Einstein')
guests.insert(0, 'Stephen Hawking')

# for guest in guests:
#   print(f"Hello {guest}, would you like to have dinner with me?")

## Exercise 3.6
moreGuests = ['Marie Curie', 'Ada Lovelace', 'Grace Hopper']

guests.insert(0, moreGuests[0])
                            
middleOfArray = len(guests) // 2
guests.insert(middleOfArray, moreGuests[1])

guests.append(moreGuests[2])

# for guest in guests:
#   print(f"Hello {guest}, would you like to have dinner with me?")

## Exercise 3.7
for guest in guests:
  print("I can only invite two people for dinner.")
  while len(guests) > 2:
    removedGuest = guests.pop()
    print(f"Sorry {removedGuest}, I can't invite you to dinner.")
  for guest in guests:
    print(f"Sorry for the incovenience {guest}, you are still invited.")
  break

del guests[0]
del guests[0]

print("Final array: ", guests)

# Exercises 3.8-3.10
places = ['Sydney', 'Paris', 'London', 'New York', 'Tokyo']

sortedPlaces = sorted(places)
sortedPlaces.reverse()
print("Original array: ", places)
print("Sorted array: ", sortedPlaces)

sortedPlaces.reverse()
print("Original array: ", places)
print("Sorted array: ", sortedPlaces)
