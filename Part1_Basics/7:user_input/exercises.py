# Exercise 7-1. 
car_input = input("What kind of car would you like to rent? ")
print(f"Let me see if I can find you a {car_input.title()}.")

# Exercise 7-2.
dinner_group = int(input("How many people are in your dinner group? "))
if dinner_group > 8:
    print("You'll have to wait for a table.")
else:
    print("Your table is ready.")

# Exercise 7-3.
number = int(input("Enter a number: "))
if number % 10 == 0:
    print("The number is a multiple of 10.")
else:
    print("The number is not a multiple of 10.")

# Exercise 7-4.
toppings_list = []

while (True):
  topping = input(f"What toppings would you like with your pizza? "
                  f"press q at anytime to quit ")
  if topping == "q":
    break
  else: 
    toppings_list.append(topping)

print(toppings_list)

# Exercise 7.5
while(True):
  age_input = int(input("Please input you age "))
  if age_input < 3:
    ticket_price = 0
  elif 3 < age_input < 12:
    ticket_price = 10
  else:
    ticket_price = 15
  break

if ticket_price != 0:
  print(f"Ticket price is {ticket_price}")
else: 
  print(f"Free entry")

# Exercise 7.6
ticket_ammount = int(input("How many tickets would you like? "))
ticket_price = 0

while(ticket_ammount > 0):
  print(f"Tickets left: {ticket_ammount} \n"
        f"Total ammount acummulated: {ticket_price}")
  age_input = input(f"Please input you age \n"
    f"press q at anytime to quit \n")
  
  if age_input == "q":
    break
  elif int(age_input) < 3:
    ticket_price += 0
    ticket_ammount -= 1
  elif 3 < int(age_input) < 12:
    ticket_price += 10
    ticket_ammount -= 1
  else:
    ticket_price += 15
    ticket_ammount -= 1 

# Exercise 7.7
# while(True):
#   print("Infinite loop")

# Exercise 7.8 -7.9
sandwich_orders = ["tuna", "ham", "cheese", "pastrami", "pastrami", "pastrami"]
finished_sandwiches = []

print("The deli has runed out of pastrami")
while "pastrami" in sandwich_orders:
  sandwich_orders.remove("pastrami")

while sandwich_orders:
  sandwich = sandwich_orders.pop()
  finished_sandwiches.append(sandwich)
  print(f"I made your {sandwich} sandwich")

print(f" This are the sandwiches i maded: {finished_sandwiches}")
print(f" This are the sandwiches that still pending: {sandwich_orders}")

#Exercise 7.10
results = []

while(True):
  place = input(f"If you could visit one place in the world where would you go?\n"
                "press q at anytime to quit \n")
  if place == "q":
    break
  else:
    results.append(place)

print(results)
