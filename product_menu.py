import json
import textwrap
from collections import defaultdict


def load_data_from_product():
    try:
        file = open('baker_product_keeping.txt', 'r')  # open the file and read
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


product_data = load_data_from_product()





# Format the data retrieve from inventory product.txt
def format_product_data(product, details):
    with open(details, 'r') as file:
        info = json.load(file)
        for detail in info.values():
            if product['product_name'] == detail['product_name']:
                description_info = detail['description']
                price = detail['price']
                break
            else:
                description_info = '-'
                price = '-'
    return (
        f"{product['product_code']} - {product['product_name'].title():<45}{price}\n"
        f"{'Best Before':<12}: {product['expiry_date']}\n"
        f"{'Allergen':<12}: {', '.join(allergen.replace('_', ' ').title() for allergen in product['allergens'])}\n"
        f"🥑 {description_info}"
    )


# Wrap the formatted data if it exceeds the space of 60 characters
def wrap_data(formatted_product_data, width=65):
    wrapped_lines = []
    for data in formatted_product_data:
        wrapped_lines.extend(textwrap.wrap(data, width=width))
    return wrapped_lines


# Format to print data retrieve from category_group dictionary side by side
def print_in_column(info1, info2, width=65):
    max_line = len(info1)
    if len(info2) > max_line:
        max_line = len(info2)
    new_info1 = info1 + [""] * (max_line - len(info1))
    new_info2 = info2 + [""] * (max_line - len(info2))

    for line1, line2 in zip(new_info1, new_info2):
        print(f'{line1.ljust(width + 8)}{line2.ljust(width)}')


def menu():
    print('\n'+'•'*55, ' Morning Glory Bakery Menu ', '•'*55, '\n')
    print('✨ We offer a delightful selection of fresh breads, cakes, pastries, biscuits, and muffins, all baked daily to satisfy your cravings.')
    print("✨ Explore our menu, and don't forget to check out our unique creations in the 'Others' category for something special!\n")

    category_groups = defaultdict(list)
    product_details = 'manager_product_inventory.txt'
    for value in product_data.values():
        category_groups[value['category']].append(format_product_data(value, product_details).split('\n'))

    for category, products in category_groups.items():

        print(f'\n📍 {category} 📍\n')

        for i in range(0, len(products), 2):
            product1 = wrap_data(products[i], width=65)
            if i + 1 < len(products):
                product2 = wrap_data(products[i + 1], width=65)
            else:
                product2 = []

            print_in_column(product1, product2)

            if i == len(products) - 1:
                print('\n'+'-'*139)
            else:
                print('\n'+'-'*139)


#menu()
