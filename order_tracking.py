import json


# Define the function that loads data from the file
def load_data_from_tracking():
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(content)  # parse the content as json format into python dictionary
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

    while True:
        order_id = input('Enter your Order ID: ')  # Prompt the customer to enter their order ID

        # Search for the order by order_id
        order_found = False
        for order_key, order in orders.items():
            if order['order_id'] == order_id:  # Compare the input with the order_id in the order details
                print(f'\n{"Order Details":^30}')
                print('-' * 55)
                print(f'{"Order ID:":<20} {order_id}')
                print(f'{"Username:":<20} {order["username"]}')
                print(f'{"Items Ordered:":<20} {", ".join(order["items_ordered"])}')
                print(f'{"Total Price:":<20} RM{order["total_price (RM)"]:.1f}')
                print(f'{"Status:":<20} {order["status"]}')
                print('-' * 55)
                order_found = True
                break  # Exit the loop when a matching order is found

        if order_found:
            break  # Exit the outer loop after displaying the order details

        # Display this message if Order ID cannot be found
        print('|⚠️ Order ID cannot be found. Please check and try again!|')


#order_tracking()


