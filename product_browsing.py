import json
import re


# Define the function that loads data from the file
def load_data_from_products():
    try:
        file = open('manager_product_inventory.txt', 'r')  # open the file and read
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


products = load_data_from_products()


def browse_products():
    try:
        # Display the products to customers
        print('\nAvailable Products:')
        for product in products.values():
            print(f'Product Name: {product['product_name']}')
            print(f'Product Code: {product['product_code']}')
            print(f'Allergen: {product['allergens']}')
            print(f'Expiry Date: {product['expiry_date']}\n')

    except FileNotFoundError:
        print('Product data cannot be found.')


