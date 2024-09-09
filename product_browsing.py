import json
import re


# Define the function that loads data from the file
def load_data_from_customer():
    try:
        file = open('product_browsing.txt', 'r')  # open the file and read
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

def browse_products():
    products = load_data_from_customer()
    try:
        # Load the products from the JSON file
        with open('product_browsing.txt', 'r') as file:
            products = json.load(file)

        # Display the products to the customer
        print('\nAvailable Products:')
        for product in products:
            print(f'Product Name: {product['name']}')
            print(f'Product Code: {product['code']}')
            print(f'Price: ${product['price']}')
            print(f'Allergen: {product['allergen']}')
            print(f'Description: {product['description']}')
            print(f'Expiry Date: {product['expiry_date']}\n')

    except FileNotFoundError:
        print('Product data cannot be found.')