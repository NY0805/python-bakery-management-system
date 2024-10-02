import random
from datetime import datetime  # %I = 01-12, %H = 00-23
from system_administration_cashier import load_data_from_cashier

overall_width = 100
cashier = load_data_from_cashier()


def centered(word, width):
    if len(word) < width:
        blank_space = (width - len(word)) // 2
        print(' ' * blank_space + word + ' ' * blank_space)
    else:
        print(word)


def receipt():
    print('')
    header = ['MORNING GLORY BAKERY',
              'Reg: 219875000123 (80851-Z)',
              '51, Lorong Maplewood, Taman Springfield, 47180, Puchong, Selangor.',
              'Tel: 04-5678951',
              'Email: morningglorybakery@gmail.com',
              'CASH SALES']
    for i in header:
        centered(i, overall_width)

    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%d/%m/%Y")
    print('\n' + current_time + current_date.rjust(overall_width-len(current_date)-1))
    print('-' * overall_width)
    invoice_second_part = random.randint(1000001, 10000000)
    print('Invoice no: MGB-' + str(invoice_second_part), end='')
    for cashier_details in cashier.values():
        cashier_username = cashier_details['cashier_username']
        print('Cashier: '.rjust(overall_width-len(cashier_username)-23) + cashier_username)




receipt()
