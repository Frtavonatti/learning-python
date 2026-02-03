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
