# Exercise 9.12
from users import Users

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
