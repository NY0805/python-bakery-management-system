import json
from datetime import datetime
from manager_notifications import load_data_from_equipment_report_keeping

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
def printed_centered(info, width):
    print('-' * width)
    side_space = (width - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (width - len(info) - side_space))
    print('-' * width)


def validate_year(year):
    if year.isdigit():
        if len(year) == 4:
            return True
        else:
            print('\n+------------------------------+')
            print('|⚠️ Please enter a valid year. |')
            print('+------------------------------+')
            return False


transaction_keeping = load_data_from_cashier_transaction_keeping()
equipment_report_keeping = load_data_from_equipment_report_keeping()


#📆


def financial_management():

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    today_income = 0
    this_month_income = 0
    total_income_so_far = 0

    for receipt_details in transaction_keeping.values():
        order_date = datetime.strptime(receipt_details['order_date'], '%d/%m/%Y')  # retrieve all date from order_list
        total_income_so_far += receipt_details['total_spend(RM)']

        if order_date == datetime.now().strftime('%d/%m/%Y'):
            today_income += receipt_details['total_spend(RM)']

        if order_date.month == datetime.now().month:
            this_month_income += receipt_details['total_spend(RM)']

    while True:
        print(f'\n💰 Today\'s {"Income":<9}: RM {today_income:.2f}{"":<25}'
              f'💰 {datetime.strftime(datetime.now(), "%B")}\'s Income So Far : RM {this_month_income:.2f}')
        print(f'💸 Today\'s {"Expenses":<9}: RM {"":<29}💵 {"Total Income So Far":<24}: RM {total_income_so_far:.2f}\n')

        printed_centered('Financial Management', 95)
        print('1. Track Income\n2. Track Expenses\n3. Track Profitability\n4. Overall Financial Tracking\n5. Back to Manager Privilege')
        track_choice = input('\nWhich financial data do you want to track:\n>>> ')
        if track_choice == '1':
            while True:
                try:
                    custom_year_for_income = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                    if int(custom_year_for_income) == 0:
                        break

                    elif validate_year(custom_year_for_income):
                        custom_month_for_income = input('\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                        if custom_month_for_income.lower() == 'cancel':
                            continue
                        while custom_month_for_income not in months:
                            print('\n+-------------------------------------+')
                            print('|⚠️ Invalid month. Please enter again. |')
                            print('+--------------------------------------+')
                            custom_month_for_income = input('\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                            if custom_month_for_income.lower() == 'cancel':
                                break

                        if custom_month_for_income in months:
                            income_of_that_month = 0
                            for receipt_details in transaction_keeping.values():
                                chosen_date = datetime.strptime(receipt_details['order_date'], '%d/%m/%Y')
                                if chosen_date.strftime("%B") == custom_month_for_income and chosen_date.year == custom_year_for_income:
                                    income_of_that_month += receipt_details['total_spend(RM)']
                            print(f'\n💰 {custom_year_for_income} {custom_month_for_income.title()} Income: RM {income_of_that_month:.2f}')
                except ValueError:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid year. Please enter again. |')
                    print('+-------------------------------------+')

        elif track_choice == '2':
            while True:
                try:
                    custom_year_for_expenses = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                    if int(custom_year_for_expenses) == 0:
                        break

                    elif validate_year(custom_year_for_expenses):
                        custom_month_for_expenses = input('\nInsert a month (or enter "cancel" to reseelct year):\n>>> ').title()
                        if custom_month_for_expenses.lower() == 'cancel':
                            continue
                        while custom_month_for_expenses not in months:
                            print('\n+-------------------------------------+')
                            print('|⚠️ Invalid month. Please enter again. |')
                            print('+--------------------------------------+')
                            custom_month_for_expenses = input('\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                            if custom_month_for_expenses.lower() == 'cancel':
                                break

                        if custom_month_for_expenses in months:
                            expenses_of_that_month = 0
                            for equipment_details in equipment_report_keeping.values():
                                unit, repair_cost = equipment_details['repair_cost'].split(' ')
                                chosen_date = datetime.strptime(equipment_details['report_date'], '%d-%m-%Y')
                                if chosen_date.strftime("%B") == custom_month_for_expenses and chosen_date.year == custom_year_for_expenses:
                                    expenses_of_that_month += float(repair_cost)
                            print(f'\n💰 {custom_year_for_expenses} {custom_month_for_expenses.title()} Expenses: RM {expenses_of_that_month:.2f}')

                except ValueError:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid year. Please enter again. |')
                    print('+-------------------------------------+')

        elif track_choice == '3':
            pass

        elif track_choice == '4':
            while True:
                try:
                    custom_year_for_overview = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                    if int(custom_year_for_overview) == 0:
                        break

                    elif validate_year(custom_year_for_overview):
                        headers = ['Date', 'Description', 'Income(RM)', 'Expenses(RM)']
                        printed_centered(f'{custom_year_for_overview} FINANCIAL REPORT', 73)
                        print(f'{headers[0]:<15}{headers[1]:<25}{headers[2]:<20}{headers[3]}')
                        print('-' * 73 + '\n')

                except ValueError:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid year. Please enter again. |')
                    print('+-------------------------------------+')


financial_management()