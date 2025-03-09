# Exercise 1
filename = 'some_words.txt'

with open(filename) as file:
  file_content = file.read()
  for times in range(3):
    print(file_content)

#Exercise 2
with open(filename) as file:
  file_content = file.read()
  replaced = file_content.replace('python', 'c')
  print(replaced)

#Exercise 3
guest = 'guest.txt'
user_input = input('Enter your name: ')

with open(guest, 'w') as file:
    file.write(user_input)

with open(guest) as file:
    file_content = file.read()
    print(file_content)

#Exercise 4
guest_book = 'guest_book.txt'

while True:
    print('Enter "q" to quit')
    guest_book_input = input('Enter your name: ')
    if guest_book_input == 'q':
      break
    else:
      with open(guest_book, 'a') as file:
        file.write(guest_book_input + '\n')

#Exercise 5
reason = 'reasons.txt'

while True:
  print('Enter "q" to quit')
  reason_input = input('Why do you like programming? ')
  if reason_input == 'q':
    break
  else:
    with open(reason, 'a') as file:
      file.write(reason_input + '\n')

#Exercise 6-7
def addition():
  while True: 
    a = input('Enter a number: ')
    b = input('Enter another number: ')
    try:
      if a == 'q' or b == 'q':
        break
      else: 
        result = int(a) + int(b)
        print(f'Press q at any time to quit')
        print(f"The result is {result}")
    except:
      print('Inputs must be numbers')

addition()

# Exercise 8-9
cats = 'cats.txt'
dogs = 'dogs.txt'

cats_list = ['siamese', 'persian', 'egiptian']
dogs_list = ['boxer', 'bulldog', 'poodle']

def write_file(file, list):
  with open(file, 'r+') as file:
    for animal in list:
      file.write(animal + '\n')

def read_file(file):
  with open(file) as file:
    content = file.read()
    print(content)

def exec_file(file, list):
  try:
    print(f'Attempting to read file: {file}')
    read_file(file)
  except FileNotFoundError:
    # print(f'The file {file} does not exist')
    pass
  else:
    write_file(file, list)
    read_file(file)

exec_file('undefined.txt', cats_list) ## Testing the exception

# Exercise 10
with open(dogs) as file:
  file_content = file.read()
  dog_counter = file_content.count('bulldog')
  print(f'There are {dog_counter} bulldogs in the file')

# Exercise 11-12
import json

number_file = 'favorite_number.json'

def write_file(file):
  favorite_number = input("What's your favorite number? ")
  with open(file, 'w') as file:
    json.dump(favorite_number, file) 

def read_json(file):
  with open(file, 'r') as file:
    content = json.load(file)
    print(f'Your favorite number is {content}')

try:
  with open(number_file, 'r') as file:
    file_content = json.load(file)
    print(f'I know your favorite number! It\'s {file_content}')
except FileNotFoundError:
  write_file(number_file)
  read_json(number_file)
except json.JSONDecodeError:
  print("The file exists but contains invalid JSON data.")
  write_file(number_file)
  read_json(number_file)

# Exercise 13
import json

filename = 'username.json'

def get_stored_username():
  """Get stored username if available."""
  with open(filename, 'r') as file:
    content = json.load(file)
    print(content) 
    return content

def get_new_username():
  """Prompt for a new username."""
  username = input("What is your name? ")
  with open(filename, 'w') as f_obj:
    json.dump(username, f_obj)
  return username

def greet_user():
  """Greet the user by name."""
  try:
    username = get_stored_username()
    if username:
      print("Welcome back, " + username + "!")
  except json.JSONDecodeError:
    print("The file exists but contains invalid JSON data.")
    username = get_new_username()
    print("We'll remember you when you come back, " + username + "!")

greet_user()