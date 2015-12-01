import random

questions = {
    "strong": "Do ye like yer drinks strong?",
    "salty": "Do ye like it with a salty tang?",
    "bitter": "Are ye a lubber who likes it bitter?",
    "sweet": "Would ye like a bit of sweetness with yer poison?",
    "fruity": "Are ye one for a fruity finish?"
}

ingredients = {
    "strong": ["glug of rum", "slug of whisky", "splash of gin"],
    "salty": ["olive on a stick", "salt-dusted rim", "rasher of bacon"],
    "bitter": ["shake of bitters", "splash of tonic", "twist of lemon peel"],
    "sweet": ["sugar cube", "spoonful of honey", "spash of cola"],
    "fruity": ["slice of orange", "dash of cassis", "cherry on top"]
}

# Write a function to ask what style of drink a customer likes
def drinkStyle():
# The function should ask each of the questions in the questions dictionary, and gather the responses in a new dictionary.
    answers = {}

    for ingredient, question in questions.items():
        # The new dictionary should contain the type of ingredient (for example "salty", or "sweet"), mapped to a Boolean value.
        answer = input(question)
        # If the customer answers y or yes to the question then the value should be True, otherwise the value should be False.
        if 'y' or 'Y' in answer:
            answers[ingredient] = 'True'
        else:
            answers[ingredient] = 'False'

    return answers

# Write a function to construct a drink

# The function should take the preferences dictionary created in the first function as a parameter.

def drinkConstructor(preferences):

   # Inside the function you should create an empty list to represent the drink.
    drink = [ ]

# For each type of ingredient which the customer said they liked you should append a corresponding ingredient from the ingredients dictionary to the drink.
    for ingredient, preference in preferences.items():
        if 'True' in preference:
            # print(ingredient + " " + preference + " " + str(random.choice(ingredients[ingredient])))
            drink.append(str(random.choice(ingredients[ingredient])))
    # Finally the function should return the drink.
    return drink

    # To choose an ingredient from one of the ingredient lists you can use the random.choice function.

if __name__ == '__main__':

    anotherDrink = True

    while anotherDrink:
        print("Preferences(Answer Y or N):")
        preferences = drinkStyle()
        drink = drinkConstructor(preferences)
        print("Custom Drink Contents:")
        for item in drink:
            print(item)
        ask = input("what you like another?")
        if 'n' in ask:
            anotherDrink = False
