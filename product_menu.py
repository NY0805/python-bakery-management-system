import json
import textwrap
from collections import defaultdict


def load_data_from_inventory_product():
    try:
        file = open('inventory_product.txt', 'r')  # open the file and read
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


product_data = load_data_from_inventory_product()


# Format the data retrieve from inventory product.txt
def format_product_data(product):
    return (
        f"Product Name: {product['product_name'].title()}\n"
        f"Product Code: {product['product_code'[0]]}\n"
        f"Expiry Date: {product['expiry_date']}\n"
        f"Allergen: {', '.join(allergen.replace('_', ' ').title() for allergen in product['allergens'])}\n"
        f"Description: hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
    )


# Wrap the formatted data if it exceeds the space of 60 characters
def wrap_data(formatted_product_data, width=60):
    wrapped_lines = []
    for data in formatted_product_data:
        wrapped_lines.extend(textwrap.wrap(data, width=width))
    return wrapped_lines


# Format to print data retrieve from category_group dictionary side by side
def print_in_column(info1, info2, width=60):
    max_line = len(info1)
    if len(info2) > max_line:
        max_line = len(info2)
    new_info1 = info1 + [""] * (max_line - len(info1))
    new_info2 = info2 + [""] * (max_line - len(info2))

    for line1, line2 in zip(new_info1, new_info2):
        print(f'{line1.ljust(width + 10)}{line2.ljust(width)}')


def menu():
    print('\n* Welcome to Morning Glory Bakery! *\n')
    print(
        'We offer a delightful selection of fresh breads, cakes, pastries, biscuits, and muffins, all baked daily to satisfy your cravings.')
    print(
        "Explore our menu, and don't forget to check out our unique creations in the others category for something special!")

    category_groups = defaultdict(list)
    for value in product_data.values():
        category_groups[value['category']].append(format_product_data(value).split('\n'))

    for category, products in category_groups.items():
        width = 70
        print('-' * (width * 2))
        print(f'\n * Category: {category} *\n')

        for i in range(0, len(products), 2):
            product1 = wrap_data(products[i], width=60)
            if i + 1 < len(products):
                product2 = wrap_data(products[i + 1], width=60)
            else:
                product2 = []

            print_in_column(product1, product2)

            if i == len(products) - 1:
                print('')
            else:
                print('')
                print('')


menu()
