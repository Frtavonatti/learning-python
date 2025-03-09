# Exercise 9.1 - 9.4
class Restaurant():
  def __init__(self, restaurant_name, cuisine_type):
    self.restaurant_name = restaurant_name
    self.cuisine_type = cuisine_type
    self.number_served = 0

  def describe_restaurant(self):
    print(f"The restaurant {self.restaurant_name} " 
          f"especility is {self.cuisine_type}")

  def open_restaurant(self):
    print(f"{self.restaurant_name} is open")

  def set_number_served(self, updated_val):
    self.number_served = updated_val
  
  def increment_number_served(self, new_served):
    self.number_served += new_served

italian_restaurant = Restaurant("Piccola Italia", "Cucina Italiana")
italian_restaurant.describe_restaurant()
italian_restaurant.open_restaurant()
italian_restaurant.set_number_served(12)
print(italian_restaurant.number_served)
italian_restaurant.increment_number_served(7)
print(italian_restaurant.number_served)

#Exercise 9.2
lebanese_restaurant = Restaurant("Libano", "Cucina Libanese")
lebanese_restaurant.describe_restaurant()

# Exercise 9.6
class IceCreamStand(Restaurant):
  def __init__(self, restaurant_name, cuisine_type, flavors):
    super().__init__(restaurant_name, cuisine_type)
    self.flavors = flavors

  def display_flavors(self):
    print(f"Available flavors are: {self.flavors}")

ice_cream_stand = IceCreamStand("Gelateria", "Gelato", ["Vanilla", "Chocolate", "Strawberry"])
ice_cream_stand.display_flavors()

### User related exercises
# Exercise 9.3 - 9.5
class Users():
  def __init__(self, first_name, last_name):
    self.first_name = first_name
    self.last_name = last_name
    self.username = first_name[0] + last_name 
    self.login_attempts = 0
  
  def describe_user(self):
    print(f" First name: {self.first_name}\n"
          f" Last name: {self.last_name}\n"
          f" Username: {self.username}")
  
  def greet_user(self):
    print(f"Hello {self.username}")
  
  def increment_login_attempts(self):
      self.login_attempts += 1
  
  def reset_login_attempts(self):
    self.login_attempts = 0

user1 = Users("John", "Doe")
user1.describe_user()
user1.greet_user()
user1.increment_login_attempts()
user1.increment_login_attempts()
print(user1.login_attempts)
user1.reset_login_attempts()
print(user1.login_attempts)

user2 = Users("Jane", "Doe")
user2.describe_user()
user2.greet_user()

# Exercise 9.8
class Privileges():
  def __init__(self):
    self.privileges = ["can add posts", "can delete posts", "can ban users"]
  
  def show_privileges(self):
    print(self.privileges)

# Exercise 9.7
class Administrator(Users):
  def __init__(self, first_name, last_name):
    super().__init__(first_name, last_name)
    self.privileges = Privileges()

admin = Administrator("admin", "test")
admin.privileges.show_privileges()
