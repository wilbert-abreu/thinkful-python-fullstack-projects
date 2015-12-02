import sys

try:
    user_input = sys.argv[1]
    try:
        upper = int(user_input)
    except ValueError:
        upper = int(input("You must supply numeric inputs:"))
except IndexError:
    user_input = input("Enter a number here:")
    try:
        upper = int(user_input)
    except ValueError:
        upper = int(input("You must supply numeric inputs:"))

for n in range(1,upper+1):
    if n % 3 == 0 and n % 5 == 0:
        print("fizz buzz")
    elif n % 3 == 0:
        print("fizz")
    elif n % 5 == 0:
        print("buzz")
    else:
        print(n)
