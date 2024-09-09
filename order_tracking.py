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
    orders = load_data_from_tracking()

    order_id = int(input('enter id: '))

    for order in orders.values():
        if order['order_id'] == order_id:

            # Display order information
            print(f'Order ID: {order['order_id']}')
            print(f'Username: {order['username']}')
            print(f'Items ordered: {order['items_ordered']}')
            print(f'Total Price: {order['total_price']}')
            print(f'Status: {order['status']}')
            break
        else:
            print('Order ID cannot be found. Please check and try again.')

