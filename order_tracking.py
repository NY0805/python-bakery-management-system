import json
import re


# Define the function that loads data from the file
def load_data_from_tracking():
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
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

def order_tracking():
    # Prompt the user to enter their Order ID
    order_id = input('Enter your Order ID: ')
    # Load orders data
    orders = load_data_from_tracking()
    # Check if the order_id exists in the loaded orders data
    # Iterate over each order to find the matching order ID

    for order in orders.values():
        if order.keys() == order_id:

            # Display order information
            print(f'Order ID: {'order_id'}')
            print(f'Username: {'username'}')
            print(f'Items ordered: {'items_ordered'}')
            print(f'Total Price: {'total_price'}')
            print(f'Status: {'status'}')
            break
        else:
            print('Order ID cannot be found. Please check and try again.')

order_tracking()