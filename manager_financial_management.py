import json
from datetime import datetime

# Define the function that loads customers' orders data from the file
def load_data_from_cashier_transaction_keeping():
    try:
        file = open('cashier_transaction_keeping.txt', 'r')  # open the file and read
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


# define the function to print content in center
def printed_centered(info):
    print('-' * 95)
    side_space = (95 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (95 - len(info) - side_space))
    print('-' * 95)


transaction_keeping = load_data_from_cashier_transaction_keeping()


def financial_management():

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    today_income = 0
    this_month_income = 0
    total_income_so_far = 0

    for receipt_details in transaction_keeping.values():
        order_date = datetime.strptime(receipt_details['order_date'], '%d/%m/%Y')  # retrieve all date from order_list
        total_income_so_far += receipt_details['total_spend']

        if order_date == datetime.strptime(datetime.strftime(datetime.now().date(), '%d/%m/%Y'), '%d/%m/%Y'):  # if order date equals to today
            today_income += receipt_details['total_spend']

        if order_date.month == datetime.now().month:
            this_month_income += receipt_details['total_spend']

    while True:
        print(f'\n💰 Today\'s {"Income":<9}: RM {today_income:.2f}{"":<25}'
              f'💰 {datetime.strftime(datetime.now(), "%B")}\'s Income So Far : RM {this_month_income:.2f}')
        print(f'💸 Today\'s {"Expenses":<9}: RM {"":<29}💵 {"Total Income So Far":<24}: RM {total_income_so_far:.2f}\n')

        printed_centered('Financial Management')
        print('1. Track Income\n2. Track Expenses\n3. Track Profitability\n4. Overall Financial Tracking\n5. Back to Manager Privilege')
        track_choice = input('\nWhich financial data do you want to track:\n>>> ')
        if track_choice == '1':
            '''headers = ['Daily Income(RM)', 'Monthly Income(RM)', 'Total income(RM)']
            total_char = 0
            for header in headers:
                total_char += len(header)
            print('\n' + '-' * (total_char+16))
            print(f'{headers[0]:<25}{headers[1]:<25}{headers[2]}')
            print('-' * (total_char+16) + '\n')'''

            while True:
                custom_month_for_income = input('\nInsert a month in text format to track the income (or enter "cancel"):\n>>> ').title()
                if custom_month_for_income.lower() == 'cancel':
                    break

                elif custom_month_for_income not in months:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid month. Please enter again. |')
                    print('+--------------------------------------+')
                else:
                    #📆
                    income_of_that_month = 0
                    for receipt_details in transaction_keeping.values():
                        chosen_date = datetime.strptime(receipt_details['order_date'], '%d/%m/%Y')
                        if datetime.strftime(chosen_date, "%B") == custom_month_for_income:
                            income_of_that_month += receipt_details['total_spend']
                    print(f'\n💰 {custom_month_for_income.title()} Income: RM {income_of_that_month:.2f}')

        elif track_choice == '2':
            while True:
                custom_month_for_expenses = input('\nInsert a month in text format to track the expenses (or enter "cancel"):\n>>> ').title()
                if custom_month_for_expenses.lower() == 'cancel':
                    break

                elif custom_month_for_expenses not in months:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid month. Please enter again. |')
                    print('+--------------------------------------+')
                else:
                    #📆
                    expenses_of_that_month = 0
                    for receipt_details in transaction_keeping.values():
                        chosen_date = datetime.strptime(receipt_details['order_date'], '%d/%m/%Y')
                        if datetime.strftime(chosen_date, "%B") == custom_month_for_expenses:
                            expenses_of_that_month += receipt_details['total_spend']
                    print(f'\n💰 {custom_month_for_expenses.title()} Income: RM {expenses_of_that_month:.2f}')




financial_management()