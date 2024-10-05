import random
import json
from datetime import datetime  # %I = 01-12, %H = 00-23
from system_administration_cashier import load_data_from_cashier
from manager_order_management import load_data_from_customer_order_list
from manager_inventory_control import load_data_from_manager_product_inventory


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

overall_width = 100
cashier = load_data_from_cashier()
customer_info = load_data_from_customer_order_list()
inventory = load_data_from_manager_product_inventory()
transaction_keeping = load_data_from_cashier_transaction_keeping()


def centered(word, width):
    if len(word) < width:
        blank_space = (width - len(word)) // 2
        print(' ' * blank_space + word + ' ' * blank_space)
    else:
        print(word)


def receipt(customer):
    print(' ')
    header = ['MORNING GLORY BAKERY',
              'Reg: 219875000123 (80851-Z)',
              '51, Lorong Maplewood, Taman Springfield, 47180, Puchong, Selangor.',
              'Tel: 04-5678951',
              'Email: morningglorybakery@gmail.com']
    for i in header:
        centered(i, overall_width)

    print('\n' + '=' * overall_width)
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%d/%m/%Y")
    print(current_time + current_date.rjust(overall_width-len(current_date)-1))
    print(' ')
    invoice_second_part = random.randint(1000001, 10000000)
    print(f'{"Invoice no":<11}: MGB-{str(invoice_second_part)}')

    for cart_id, customer_details in customer_info.items():
        if customer in cart_id:
            username = customer_details['username']
            order_id = customer_details['order_id']
            print(f'{"Username":<11}: {username}')
            print(f'{"Order ID":<11}: {order_id}')
            print(f'{"Cart ID":<11}: {cart_id}')

    summary_header = ['Item', 'Qty', 'Price(RM)', 'Amount(RM)']
    print(f'\n{summary_header[0]:<40}{summary_header[1]:<25}{summary_header[2]:<25}{summary_header[3]}')
    print('-' * overall_width)

    total_amount = []
    for cart_id, customer_details in customer_info.items():
        if str(customer) in cart_id:
            for item in customer_details['items_ordered']:
                item_name, quantity = item.split('x')

                for product_details in inventory.values():
                    if product_details['product_name'] in item_name:
                        item_price = product_details['price'].replace('RM ', '')
                        amount = int(quantity) * float(item_price)
                        print(f'{item_name.title():<40}{quantity:<25}{item_price:<25}{amount:.2f}')
                        total_amount.append(amount)

    print('')
    print('-' * overall_width)

    subtotal = sum(total_amount)
    print(f'{"Points earned: "}{subtotal * 10:<50}{"Subtotal: ":<25}{subtotal:.2f}')

    discounted_price = 0
    print(f'{"Discount: ".rjust(75)}{"".ljust(15)}{discounted_price}')
    service_tax = subtotal * 0.06
    print(f'{"Service tax @ 6%: ".rjust(75)}{"".ljust(15)}{service_tax:.2f}')
    total = subtotal + service_tax - discounted_price
    print(f'\n{"TOTAL: ".rjust(75)}{"".ljust(15)}{total:.2f}')

    print('\n' * 3)
    warning = 'Goods sold are not returnable and refundable !'
    centered(warning, overall_width)
    appreciation = '***** Thank You Please Come Again *****'
    centered(appreciation, overall_width)

    for cart_id, customer_details in customer_info.items():
        if customer == cart_id:
            transaction_keeping[customer] = {
                "order_id": customer_details['order_id'],
                "order_date": current_date,
                "total_spend": total
            }
    save_info(transaction_keeping)


receipt(str(5580946551))
