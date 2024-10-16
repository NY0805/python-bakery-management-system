import json
from datetime import datetime
from manager_notifications import load_data_from_equipment_report_keeping
from manager_inventory_ingredient import load_data_from_inventory_ingredient
from cashier_sales_report import load_data_from_sales_report


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
ingredient_keeping = load_data_from_inventory_ingredient()
sales_report = load_data_from_sales_report()


#📆


def financial_management():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    today_income = 0
    today_expenses = 0
    this_month_income = 0
    total_income_so_far = 0

    for receipt_details in transaction_keeping.values():
        order_date = datetime.strptime(receipt_details['order_date'], '%d-%m-%Y')  # retrieve all date from order_list
        total_income_so_far += receipt_details['total_spend(RM)']

        if order_date.strftime('%d-%m-%Y') == datetime.now().strftime('%d-%m-%Y'):
            today_income += receipt_details['total_spend(RM)']

        if order_date.month == datetime.now().month:
            this_month_income += receipt_details['total_spend(RM)']

    for equipment_details in equipment_report_keeping.values():
        repair_date = equipment_details['report_date']
        unit, repair_cost = equipment_details['repair_cost'].split(' ')

        if repair_date == datetime.now().strftime('%d-%m-%Y'):
            today_expenses += float(repair_cost)

    for ingredient_details in ingredient_keeping.values():
        purchase_date = ingredient_details['purchase_date']
        unit, ingredient_cost = ingredient_details['cost_per_unit'].split(' ')
        cost = float(ingredient_cost) * ingredient_details['quantity_purchased']

        if purchase_date == datetime.now().strftime('%d-%m-%Y'):
            today_expenses += cost

    while True:
        print('')
        print(f'\n💰 Today\'s {"Income":<9}: RM {today_income:.2f}'.ljust(56) +
              f'💰 {datetime.strftime(datetime.now(), "%B")}\'s Income So Far : RM {this_month_income:.2f}')
        print(f'💸 Today\'s {"Expenses":<9}: RM {today_expenses:.2f}'.ljust(
            55) + f'💵 {"Total Income So Far":<24}: RM {total_income_so_far:.2f}\n')

        printed_centered('Financial Management', 95)
        print('1. Track Income\n2. Track Expenses\n3. Track Profitability\n4. Back to Manager Privilege')
        track_choice = input('\nWhich financial data do you want to track:\n>>> ')
        if track_choice == '1':
            while True:
                try:
                    custom_year_for_income = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                    if int(custom_year_for_income) == 0:
                        break

                    elif validate_year(custom_year_for_income):
                        custom_month_for_income = input(
                            '\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                        if custom_month_for_income.lower() == 'cancel':
                            continue
                        while custom_month_for_income not in months:
                            print('\n+-------------------------------------+')
                            print('|⚠️ Invalid month. Please enter again. |')
                            print('+--------------------------------------+')
                            custom_month_for_income = input(
                                '\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                            if custom_month_for_income.lower() == 'cancel':
                                break

                        else:
                            if custom_month_for_income in months:
                                income_of_that_month = 0
                                for receipt_details in transaction_keeping.values():
                                    chosen_date = datetime.strptime(receipt_details['order_date'], '%d-%m-%Y')
                                    if chosen_date.strftime(
                                            "%B") == custom_month_for_income and chosen_date.year == int(
                                            custom_year_for_income):
                                        income_of_that_month += receipt_details['total_spend(RM)']
                                print(
                                    f'\n💲 {custom_year_for_income} {custom_month_for_income.title()} Income: RM {income_of_that_month:.2f}')

                                headers = ['Date', 'Description', 'Income(RM)']
                                print('=' * 95)
                                print(f'{headers[0]:<35}{headers[1]:<40}{headers[2]}')
                                print('=' * 95)

                                for receipt_details in transaction_keeping.values():
                                    receipt_converted_date = datetime.strptime(receipt_details['order_date'],
                                                                               '%d-%m-%Y')
                                    if receipt_converted_date.strftime(
                                            "%B") == custom_month_for_income and receipt_converted_date.year == int(
                                            custom_year_for_income):
                                        if len(receipt_details['items']) == 1:
                                            print(
                                                f'{receipt_details["order_date"]:<35}{receipt_details["items"][0]:<40}{receipt_details["total_spend(RM)"]:.2f}')

                                        else:
                                            print(
                                                f'{receipt_details["order_date"]:<35}{receipt_details["items"][0]:<40}{""}')
                                            for item in receipt_details['items'][1:]:
                                                print(f'{"":<35}{item:<40}{receipt_details["total_spend(RM)"]:.2f}')
                                        print('-' * 95)


                                    else:
                                        print('\n❗No record found. Please select another year.')
                                        break

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
                        custom_month_for_expenses = input(
                            '\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                        if custom_month_for_expenses.lower() == 'cancel':
                            continue
                        while custom_month_for_expenses not in months:
                            print('\n+-------------------------------------+')
                            print('|⚠️ Invalid month. Please enter again. |')
                            print('+--------------------------------------+')
                            custom_month_for_expenses = input(
                                '\nInsert a month (or enter "cancel" to reselect year):\n>>> ').title()
                            if custom_month_for_expenses.lower() == 'cancel':
                                break

                        if custom_month_for_expenses in months:
                            expenses_of_that_month = 0
                            for equipment_details in equipment_report_keeping.values():
                                unit, repair_cost = equipment_details['repair_cost'].split(' ')
                                chosen_date = datetime.strptime(equipment_details['report_date'], '%d-%m-%Y')
                                if chosen_date.strftime("%B") == custom_month_for_expenses and chosen_date.year == int(
                                        custom_year_for_expenses):
                                    expenses_of_that_month += float(repair_cost)

                            for ingredient_details in ingredient_keeping.values():
                                purchase_date = datetime.strptime(ingredient_details['purchase_date'], '%d-%m-%Y')
                                unit, ingredient_cost = ingredient_details['cost_per_unit'].split(' ')
                                cost = float(ingredient_cost) * ingredient_details['quantity_purchased']
                                if purchase_date.strftime(
                                        "%B") == custom_month_for_expenses and purchase_date.year == int(
                                        custom_year_for_expenses):
                                    expenses_of_that_month += float(cost)

                            print(
                                f'\n💲 {custom_year_for_expenses} {custom_month_for_expenses.title()} Expenses: RM {expenses_of_that_month:.2f}')

                            headers = ['Date', 'Description', 'Expenses(RM)']
                            print('=' * 95)
                            print(f'{headers[0]:<35}{headers[1]:<40}{headers[2]}')
                            print('=' * 95)

                            for equipment_details in equipment_report_keeping.values():
                                equipment_converted_date = datetime.strptime(equipment_details['report_date'],
                                                                             '%d-%m-%Y')
                                cost_unit, equipment_repair_cost = equipment_details['repair_cost'].split(' ')
                                if equipment_converted_date.strftime(
                                        "%B") == custom_month_for_expenses and equipment_converted_date.year == int(
                                        custom_year_for_expenses):
                                    print(
                                        f'{equipment_details["report_date"]:<35}{equipment_details["equipment_name"]:<40}{equipment_repair_cost:.2f}')
                                    print('\n')

                            for ingredient_details in ingredient_keeping.values():
                                ingredient_purchase_date = datetime.strptime(ingredient_details['purchase_date'],
                                                                             '%d-%m-%Y')
                                ingredient_unit, ingredient_cost = ingredient_details['cost_per_unit'].split(' ')
                                ingredient_cost = float(ingredient_cost) * ingredient_details['quantity_purchased']
                                if ingredient_purchase_date.strftime(
                                        "%B") == custom_month_for_expenses and ingredient_purchase_date.year == int(
                                        custom_year_for_expenses):
                                    print(
                                        f'{ingredient_details["purchase_date"]:<35}{ingredient_details["ingredient_name"]:<40}{ingredient_cost:.2f}')
                                    print('\n')

                except ValueError:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid year. Please enter again. |')
                    print('+-------------------------------------+')

        elif track_choice == '3':
            while True:
                print('\nProfit Tracking:\n'
                      '1. Annual Profit Summary\n'
                      '2. Monthly Profit Summary\n')
                profit_type = input('Type of profit to track (1 or 2): ')

                if profit_type not in ['1', '2']:
                    print('\n+--------------------------------------+')
                    print('|⚠️ Invalid input. Please enter again. |')
                    print('+--------------------------------------+')
                    continue

                if profit_type == '1':
                    while True:
                        custom_year_for_profit = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                        try:
                            if int(custom_year_for_profit) == 0:
                                break

                            elif validate_year(custom_year_for_profit):
                                printed_centered(f'📊 {custom_year_for_profit} PROFIT SUMMARY 📊', 70)
                                total_sales = 0
                                total_orders = 0
                                for sales in sales_report.values():
                                    if sales['report_type'] == 'yearly sales report' and sales['selected_year'] == custom_year_for_profit:
                                        total_sales += sales['total_sales']
                                        total_orders += sales['total_order']

                                print(f'Total sales: RM {total_sales:.2f} ({total_orders} orders)')

                                total_repair_cost = 0
                                total_ingredient_cost = 0
                                for equipment_details in equipment_report_keeping.values():
                                    if (datetime.strptime(equipment_details['report_date'], '%d-%m-%Y').year == int(custom_year_for_profit)):
                                        unit, equipment_cost = equipment_details['repair_cost'].split(' ')
                                        total_repair_cost += float(equipment_cost)

                                for ingredient_details in ingredient_keeping.values():
                                    unit, ingredient_cost = ingredient_details['cost_per_unit'].split(' ')
                                    cost = float(ingredient_cost) * ingredient_details['quantity_purchased']
                                    if (datetime.strptime(ingredient_details['purchase_date'], '%d-%m-%Y').year == int(
                                            custom_year_for_profit)):
                                        total_ingredient_cost += float(cost)

                                print(f'Total expenses: RM {total_repair_cost + total_ingredient_cost:.2f}\n')
                                print('-' * 70)

                                net_profit = total_sales - (total_repair_cost + total_ingredient_cost)
                                print(f'Net profit: RM {net_profit:.2f}')

                                profit_margin = (net_profit/total_sales) * 100
                                print(f'Profit margin: RM {profit_margin:.2f}')

                                if net_profit < 0:
                                    print('Cashflow: ')

                        except ValueError:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')

                elif profit_type == '2':
                    pass


        elif track_choice == '4':
            print('\nExiting to Manager Privilege......')
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


financial_management()
