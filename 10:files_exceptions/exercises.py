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

