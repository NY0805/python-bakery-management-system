import json


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
    print('\n-----------------------------------------------')
    print('\t\t\t', 'ORDER TRACKING')
    print('-----------------------------------------------')
    print()
    order_id = input('Enter your order ID: ')  # Keep order_id as a string

    # Check whether the order ID exists in the order dictionary.
    if order_id in orders:
        order = orders[order_id]  # Get the order details
        # Display order information
        print(f'Order ID: {order_id}')
        print(f'Username: {order["username"]}')  # Use double quotes here
        print(f'Items ordered: {order["items_ordered"]}')  # Use double quotes here
        print(f'Total Price: RM{order["total_price"]:.2f}')  # Use double quotes here
        print(f'Status: {order["status"]}')  # Use double quotes here
    else:
        print('|⚠️Order ID cannot be found. Please check and try again!|')


order_tracking()