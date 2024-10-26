import random
import json
from datetime import datetime  # %I = 01-12, %H = 00-23
from system_administration_cashier import load_data_from_cashier
from manager_order_management import load_data_from_customer_order_list
from manager_inventory_control import load_data_from_manager_product_inventory
from cashier_discount_management import discount_management


def load_data_from_cashier_transaction_keeping():
    try:
        file = open('cashier_transaction_keeping.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def save_info(transaction_keeping):
    file = open('cashier_transaction_keeping.txt', 'w')  # open the file to write
    json.dump(transaction_keeping, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


terminal_width = 100  # initiate the width of display panel
cashier = load_data_from_cashier()  # store the data that retrieved from file into cashier
inventory = load_data_from_manager_product_inventory()  # store the data that retrieved from file into inventory
transaction_keeping = load_data_from_cashier_transaction_keeping()  # store the data that retrieved from file into transaction_keeping
discount_management = discount_management()


# define a function to arrange the content in the center
def centered(word, width):
    if len(word) < width:
        blank_space = (width - len(word)) // 2  # calculate the blank space required to make the content to be centered. Floor division is used to avoid decimal
        print(' ' * blank_space + word + ' ' * blank_space)  # shows how the content will be displayed
    else:
        print(word)  # ignore all the calculation and display the content directly if the length of content exceed the width of display panel initiated before


# define the format of displaying the receipt
def receipt(customer):
    customer_info = load_data_from_customer_order_list()  # store the data that retrieved from file into customer_info
    print(' ')
    # header of the receipt
    header = ['MORNING GLORY BAKERY',
              'Reg: 219875000123 (80851-Z)',
              '51, Lorong Maplewood, Taman Springfield, 47180, Puchong, Selangor.',
              'Tel: 04-5678951',
              'Email: morningglorybakery@gmail.com',
              'Business hours: 9.00AM - 6.00PM']
    print('')
    print('-' * terminal_width)
    for i in header:
        centered(i, terminal_width)  # call the function to print the header in the middle

    print('\n' + '=' * terminal_width)  # print a separate line
    current_time = datetime.now().strftime("%I:%M:%S %p")  # convert the time into string for readability and store it into "current_time" variable.If not in string, it will display 13:45:45.123456
    current_date = datetime.now().strftime("%d-%m-%Y")  # convert the date into string for self-formatting and store it into "current_date" variable
    print(current_time + current_date.rjust(terminal_width-len(current_date)-1))  # specify the format of printing date and time
    print(' ')  # blank a line
    receipt_no = random.randint(1000001, 10000000)  # determine the invoice number in random in a range from 1000001 to 10000000
    print(f'{"Receipt no":<11}: MGB-{str(receipt_no)}')

    for cart_id, customer_details in customer_info.items():
        if customer in cart_id:
            username = customer_details['username']
            order_id = customer_details['order_id']
            print(f'{"Username":<11}: {username}')
            print(f'{"Order ID":<11}: {order_id}')
            print(f'{"Cart ID":<11}: {cart_id}')

    # add the header of the table that used to display details in a list
    summary_header = ['Item', 'Qty', 'Price(RM)', 'Amount(RM)']
    print(f'\n{summary_header[0]:<40}{summary_header[1]:<25}{summary_header[2]:<25}{summary_header[3]}')  # print the table header in a custom format, with determining the spaces needed among the words
    print('-' * terminal_width)  # print a separate line

    # create a list to store the total amount to pay for each item
    total_amount = []
    for cart_id, customer_details in customer_info.items():
        if str(customer) in cart_id:
            for item in customer_details['items_ordered']:
                item_name, quantity = item.split('x')  # split the item into 2 parts by the separator 'x', store the splitted values in item_name and quantity

                for product_details in inventory.values():
                    if product_details['product_name'] in item_name:
                        item_price = product_details['price'].replace('RM ', '')  # 'RM' is replaced with empty since it is mentioned in the table header
                        amount = int(quantity) * float(item_price)  # calculate the amount of each item by multiplying the quantity and the price
                        print(f'{item_name.title():<40}{quantity:<25}{item_price:<25}{amount:.2f}')  # print the details in a custom format
                        total_amount.append(amount)  # append the amount of each item into the list "total_amount"

    print('')
    print('-' * terminal_width)

    # calculate subtotal by adding the amount in "total_amount"
    subtotal = 0
    for amount in total_amount:
        subtotal += amount

    print(f'{"":<65}{"Subtotal: ":<25}{subtotal:.2f}')
    total_discount_price = 0
    non_discount_price = 0
    if str(customer) in customer_info:
        customer_details = customer_info[str(customer)]
        for discounts in discount_management.values():
            unit, price = discounts['Price'].split(' ')
            discount_value, percentage = discounts['Discount'].split('%')

            for item in customer_details['items_ordered']:
                item_name, quantity = item.split('x')  # split the item into 2 parts by the separator 'x', store the splitted values in item_name and quantity

                if item_name.strip() == discounts['Product Name'].strip():

                    if float(discount_value) != 0:
                        discounted_price = (float(price) - (float(price) * float(discount_value))/100) * int(quantity)
                        total_discount_price += discounted_price
                    else:
                        non_discount_price += (float(price) * int(quantity))

    print(f'{"Discounted price: ".rjust(75)}{"".ljust(15)}{non_discount_price+total_discount_price:.2f}')  # assign the corresponding new value to discounted_price if customers want to redeem their price
    service_tax = (non_discount_price + total_discount_price) * 0.06  # calculate the service tax

    print(f'{"Service tax @ 6%: ".rjust(75)}{"".ljust(15)}{service_tax:.2f}')
    total = non_discount_price + total_discount_price + service_tax  # calculate the final amount that need to be paid by customers
    print(f'\n{"Points earned: "}{int((non_discount_price + total_discount_price) * 10)}{"TOTAL: ".rjust(57)}{"".ljust(15)}{total:.2f}')

    print('\n' * 3)
    warning = 'Goods sold are not returnable and refundable !'  # message that warning customers the items are not returnable and refundable
    centered(warning, terminal_width)  # print the warning message in the center according to the customize display panel's width
    appreciation = '***** Thank You Please Come Again *****'  # express the appreciation to customers
    centered(appreciation, terminal_width)  # print the appreciation in the center according to the customize display panel's width
    print('-' * terminal_width)
    print('')

    # determine the format of data as dictionary format to be saved to the file
    for cart_id, customer_details in customer_info.items():
        if customer == cart_id:
            transaction_keeping[f'MGB-{receipt_no}'] = {
                "order_id": customer_details['order_id'],
                "items": customer_details['items_ordered'],
                "order_date": current_date,
                "total_spend(RM)": f'{total:.2f}'
            }
    save_info(transaction_keeping)  # save the data

#receipt(str(4992374927))

