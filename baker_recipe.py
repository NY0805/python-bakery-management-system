import json
import re
from collections import defaultdict
import baker_inventory_ingredient

# Define the function that loads data from the file
def load_data_from_recipe():
    try:
        file = open('recipe.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def load_data_from_inventory_ingredient():
    try:
        file = open('inventory_ingredient.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def save_info(baker_recipe):
    file = open('customer.txt', 'w')  # open the file to write
    json.dump(recipe, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('Please enter something...\n')
        return False


def validation_alphanum_only(info):
    if info.isalnum():
        return True
    else:
        return False


def validation_alphabet_only(info):
    if re.search(r'[A-Za-z ]+', info):
        return True
    else:
        return False


def validation_list_alphabet_only(info):
    for item in info:
        if re.search(r'[A-Za-z ]+', item):
            return True
        else:
            return False


def validation_digit_only(info):
    if info.isdigit():
        return True
    else:
        return False


def format_ingredient_data(product):
    return (
        f"Product Name: {product['product_name'].title()}\n"
    )


ingredient_list = load_data_from_inventory_ingredient()

ingredient_category_groups = defaultdict(list)
for value in ingredient_list.values():
    ingredient_category_groups[value['category']].append(format_ingredient_data(value).split('\n'))


def recipe():
    recipe_info = ['Recipe Name', 'Categories', 'Ingredient_Per_Unit', 'Variation', 'Notes']

    max_length = 0
    for item in recipe_info:
        if len(item) > max_length:
            max_length = len(item)

    while True:
        recipe_name = input(f'1. {recipe_info[0].ljust(max_length + 2)}: ')
        if validation_empty_entries(recipe_name):
            if validation_alphabet_only(recipe_name):
                break
            else:
                print('Please enter a valid recipe name. (Cannot contain any digits and special characters.)\n')

    while True:
        print('* Categories: Breads, Cakes, Pastries, Biscuits, Muffins, Others *')
        category = input(f'2. {recipe_info[1].ljust(max_length + 2)}: ')
        if validation_empty_entries(category):
            match = re.match(r'[A-Za-z]+$', category.strip())
            if match:
                if category in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                    break
                else:
                    print('Please enter a valid category based on the categories given. (Case sensitive.)\n')
            else:
                print("Please enter a valid category. (Cannot contain any spacing, digits and special characters.)\n")

    while True:
        print('Here are the ingredient list: ')
        for category, item in ingredient_category_groups.items():
            print(f'* Category: {category} *')
            for i in item:
                print(format_ingredient_data(i))

        ingredient_per_unit = []
        ingredient_per_unit = input(f'3. {recipe_info[2].ljust(max_length + 2)}: ')
        if validation_empty_entries(category):
            match = re.match(r'[A-Za-z]+$', category.strip())
            if match:
                if category in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                    break
                else:
                    print('Please enter a valid category based on the categories given.\n')
            else:
                print(
                    "Please enter a valid category. (Case sensitive. Cannot contain any spacing, digits and special characters.)\n")


recipe()

