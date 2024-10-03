import json


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
    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'PRODUCT BROWSING')
    print('-----------------------------------------------')
    try:
        # Display the products available to customers
        print('\nAvailable Products:')
        print('-----------------------------------------------')

        for product_code, product in products.items():  # Get the product code from the dictionary key
            print(f'Product Code: {product_code}')
            print(f'Product Name: {product["product_name"]}')
            print(f'Stock: {product["stock"]}')
            print(f'Price: {product["price"]}')
            print(f'Description: {product["description"]}')
            print('-----------------------------------------------')

    except FileNotFoundError:
        print('|⚠️Product data cannot be found.|')

browse_products()



