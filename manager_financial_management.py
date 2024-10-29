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


# define a function to validate the year in 4 digits
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


def financial_management():
    # create a list to store the months
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    # initialize the variables to 0 for calculation later
    today_income = 0
    today_expenses = 0
    this_month_income = 0
    total_income_so_far = 0

    for receipt_details in transaction_keeping.values():
        order_date = datetime.strptime(receipt_details['order_date'], '%d-%m-%Y')  # retrieve all date from order_list
        total_income_so_far += float(receipt_details['total_spend(RM)'])  # add all value of 'total_spend' to the variable

        if order_date.strftime('%d-%m-%Y') == datetime.now().strftime('%d-%m-%Y'):
            today_income += float(receipt_details['total_spend(RM)'])  # add the value to today_income if the order_date is current date

        if order_date.month == datetime.now().month:
            this_month_income += float(receipt_details['total_spend(RM)'])  # add the value to this_month_income if the month of order_date is current month

    for equipment_details in equipment_report_keeping.values():
        repair_date = equipment_details['report_date']
        unit, repair_cost = equipment_details['repair_cost'].split(' ')  # split the cost into unit and value

        if repair_date == datetime.now().strftime('%d-%m-%Y'):
            today_expenses += float(repair_cost)  # add the value to today_expenses if repair_date is current date

    for ingredient_details in ingredient_keeping.values():
        purchase_date = ingredient_details['purchase_date']
        unit, ingredient_cost = ingredient_details['cost_per_unit'].split(' ')
        cost = float(ingredient_cost) * ingredient_details['quantity_purchased']  # calculate the cost for every ingredient purchased

        if purchase_date == datetime.now().strftime('%d-%m-%Y'):
            today_expenses += cost  # add the calculated cost to today_expenses if the purchase_date is current date

    while True:
        # display the result of the calculation
        print('')
        print(f'\n💰 Today\'s {"Income":<9}: RM {today_income:.2f}'.ljust(56) +
              f'💰 {datetime.strftime(datetime.now(), "%B")}\'s Income So Far : RM {this_month_income:.2f}')
        print(f'💸 Today\'s {"Expenses":<9}: RM {today_expenses:.2f}'.ljust(
            55) + f'💵 {"Total Income So Far":<24}: RM {total_income_so_far:.2f}\n')

        printed_centered('Financial Management', 95)
        print('1. Track Income\n2. Track Expenses\n3. Track Profitability\n4. Back to Manager Privilege')
        track_choice = input('\nWhich financial data do you want to track:\n>>> ')
        if track_choice == '1':  # track income is chosen
            while True:
                try:
                    custom_year_for_income = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                    if int(custom_year_for_income) == 0:  # cancel to track income
                        break

                    elif validate_year(custom_year_for_income):
                        custom_month_for_income = input(
                            '\nInsert the name of a month (or enter "cancel" to reselect year):\n>>> ').title()
                        if custom_month_for_income.lower() == 'cancel':
                            continue
                        while custom_month_for_income not in months:
                            print('\n+-------------------------------------+')
                            print('|⚠️ Invalid month. Please enter again. |')
                            print('+--------------------------------------+')
                            custom_month_for_income = input(
                                '\nInsert the name of a month (or enter "cancel" to reselect year):\n>>> ').title()
                            if custom_month_for_income.lower() == 'cancel':
                                break

                        else:
                            # process to calculate the income of the requested year and month
                            if custom_month_for_income in months:
                                income_of_that_month = 0
                                for receipt_details in transaction_keeping.values():
                                    chosen_date = datetime.strptime(receipt_details['order_date'], '%d-%m-%Y')
                                    if chosen_date.strftime(
                                            "%B") == custom_month_for_income and chosen_date.year == int(
                                            custom_year_for_income):
                                        income_of_that_month += float(receipt_details['total_spend(RM)'])

                                # display the result of the income
                                print(
                                    f'\n💲 {custom_year_for_income} {custom_month_for_income} Income: RM {income_of_that_month:.2f}')

                                headers = ['Date', 'Description', 'Income(RM)']
                                print('=' * 95)
                                print(f'{headers[0]:<35}{headers[1]:<40}{headers[2]}')
                                print('=' * 95)

                                for receipt_details in transaction_keeping.values():
                                    receipt_converted_date = datetime.strptime(receipt_details['order_date'],
                                                                               '%d-%m-%Y')

                                    # no record found if the requested year and month not in file
                                    if custom_month_for_income not in receipt_converted_date.strftime("%B") and custom_year_for_income not in receipt_converted_date.strftime("%Y"):
                                        print('\n❗No record found. Please select another year.')
                                        break

                                    # otherwise, display the income record in table form
                                    elif receipt_converted_date.strftime(
                                            "%B") == custom_month_for_income and receipt_converted_date.year == int(custom_year_for_income):
                                        if len(receipt_details['items']) == 1:
                                            print(
                                                f'{receipt_details["order_date"]:<35}{receipt_details["items"][0]:<40}{receipt_details["total_spend(RM)"]:.2f}')

                                        else:
                                            print(
                                                f'{receipt_details["order_date"]:<35}{receipt_details["items"][0]:<40}{""}')
                                            for item in receipt_details['items'][1:]:
                                                print(f'{"":<35}{item:<40}{receipt_details["total_spend(RM)"]:.2f}')
                                        print('\n')

                except ValueError:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid year. Please enter again. |')
                    print('+-------------------------------------+')

        elif track_choice == '2':  # track expenses is chosen
            while True:
                try:
                    custom_year_for_expenses = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                    if int(custom_year_for_expenses) == 0:
                        break

                    elif validate_year(custom_year_for_expenses):
                        custom_month_for_expenses = input(
                            '\nInsert the name of a month (or enter "cancel" to reselect year):\n>>> ').title()
                        if custom_month_for_expenses.lower() == 'cancel':
                            continue
                        while custom_month_for_expenses not in months:
                            print('\n+-------------------------------------+')
                            print('|⚠️ Invalid month. Please enter again. |')
                            print('+--------------------------------------+')
                            custom_month_for_expenses = input(
                                '\nInsert the name of a month (or enter "cancel" to reselect year):\n>>> ').title()
                            if custom_month_for_expenses.lower() == 'cancel':
                                break

                        # process to calculate the expenses on ingredients and equipment of the requested year and month
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

                            # display the result of the expenses
                            print(
                                f'\n💲 {custom_year_for_expenses} {custom_month_for_expenses.title()} Expenses: RM {expenses_of_that_month:.2f}')

                            headers = ['Date', 'Description', 'Expenses(RM)']
                            print('=' * 95)
                            print(f'{headers[0]:<35}{headers[1]:<40}{headers[2]}')
                            print('=' * 95)

                            # display the expenses record in table form
                            for equipment_details in equipment_report_keeping.values():
                                equipment_converted_date = datetime.strptime(equipment_details['report_date'],
                                                                             '%d-%m-%Y')
                                cost_unit, equipment_repair_cost = equipment_details['repair_cost'].split(' ')
                                if equipment_converted_date.strftime(
                                        "%B") == custom_month_for_expenses and equipment_converted_date.year == int(
                                        custom_year_for_expenses):
                                    print(
                                        f'{equipment_details["report_date"]:<35}{equipment_details["equipment_name"]:<40}{float(equipment_repair_cost):.2f}')
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
                            # no record found if the requested year and month not in file
                            if expenses_of_that_month == 0:
                                print('\n❗No record found. Please select another year.')

                except ValueError:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Invalid year. Please enter again. |')
                    print('+-------------------------------------+')

        elif track_choice == '3':  # track profitability is chosen
            while True:
                print('\nProfit Tracking:\n'
                      '1. Annual Profit Summary\n'
                      '2. Monthly Profit Summary\n')
                profit_type = input('Type of profit to track (1, 2 or "cancel"): ')

                if profit_type not in ['1', '2', 'cancel']:
                    print('\n+--------------------------------------+')
                    print('|⚠️ Invalid input. Please enter again. |')
                    print('+--------------------------------------+')
                    continue

                if profit_type == '1':  # track annual profit
                    while True:
                        custom_year_for_profit = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                        try:
                            if int(custom_year_for_profit) == 0:
                                break

                            elif validate_year(custom_year_for_profit):
                                print('')
                                printed_centered(f'📊 {custom_year_for_profit} PROFIT SUMMARY 📊', 85)
                                total_sales = 0
                                total_orders = 0
                                # calculate the total sales snd total order for the year requested
                                for sales in sales_report.values():
                                    if sales['report_type'] == 'yearly sales report' and sales['selected_year'] == custom_year_for_profit:
                                        total_sales += sales['total_sales']
                                        total_orders += sales['total_order']

                                print(f'Total sales: RM {total_sales:.2f} ({total_orders} orders)')  # display the result

                                # process to calculate the expenses on ingredients and equipment repair for the requested year
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

                                # display the calculated result
                                print(f'Total expenses: RM {total_repair_cost + total_ingredient_cost:.2f}\n')
                                print('-' * 85)

                                # inform how net profit is calculated
                                net_profit = total_sales - (total_repair_cost + total_ingredient_cost)
                                if net_profit < 0:  # net profit results in negative
                                    print(f'Net profit: RM {net_profit:.2f} (deficit)')
                                elif net_profit > 0:  # net profit results in positive
                                    print(f'Net profit: RM {net_profit:.2f} (surplus)')
                                else:
                                    # net profit results in 0
                                    print(f'Net profit: RM {net_profit:.2f} (break-even point)')

                                try:
                                    # inform how profit margin is calculated
                                    profit_margin = (net_profit/total_sales) * 100
                                    print(f'Profit margin: {profit_margin:.2f}%\n')  # display the result of profit margin

                                    if profit_margin < 0:  # profit margin is negative
                                        print(f'The bakery lost approximately RM {profit_margin/100:.2f} for every RM earned.')
                                        print('❗ It is a significant loss. Please pay immediate attention to this financial issues.')
                                    elif profit_margin > 0:  # profit margin is positive
                                        print(f'The bakery make RM {profit_margin/100:.2f} for every RM earned.')
                                        print('🎊 Congrats! The business is healthy and sustainable.')
                                    else:
                                        # profit margin is 0
                                        print(f'The bakery is not making any profit.')
                                        print('A robust business strategy is needed to enhance the profitability in the future.')

                                    print('\n' + '-' * 85)

                                except ZeroDivisionError:  # handle the error if a value is divided by 0
                                    print('\n⚠️ The profit margin cannot be calculated as it has no income.')

                        except ValueError:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')

                elif profit_type == '2':  # track monthly profit
                    while True:
                        try:
                            chosen_year = input('\nInsert a year (or enter "0" to cancel):\n>>> ')
                            if int(chosen_year) == 0:
                                break
                            elif validate_year(chosen_year):
                                custom_month_for_profit = input('\nInsert the name of a month:\n>>> ').title()

                                if custom_month_for_profit in months:
                                    print('')
                                    printed_centered(f'📆 {chosen_year} {custom_month_for_profit} PROFIT SUMMARY 📆', 85)
                                    # calculate the total sales snd total order for the year and month requested
                                    monthly_sales = 0
                                    monthly_orders = 0
                                    for sales in sales_report.values():
                                        converted_month = datetime.strptime(custom_month_for_profit, '%B').month
                                        if sales['report_type'] == 'monthly sales report' and int(sales['selected_month']) == converted_month:
                                            monthly_sales += sales['total_sales']
                                            monthly_orders += sales['total_order']

                                    print(f'Total monthly sales: RM {monthly_sales:.2f} ({monthly_orders} orders)')  # display the result

                                    # process to calculate the expenses on ingredients and equipment repair for the requested year and month
                                    monthly_repair_cost = 0
                                    monthly_ingredient_cost = 0
                                    for equipment_details in equipment_report_keeping.values():
                                        converted_report_date = datetime.strptime(equipment_details['report_date'], '%d-%m-%Y')
                                        if converted_report_date.strftime('%B') == custom_month_for_profit:
                                            unit, equipment_cost = equipment_details['repair_cost'].split(' ')
                                            monthly_repair_cost += float(equipment_cost)

                                    for ingredient_details in ingredient_keeping.values():
                                        converted_purchase_date = datetime.strptime(ingredient_details['purchase_date'], '%d-%m-%Y')
                                        unit, ingredient_cost = ingredient_details['cost_per_unit'].split(' ')
                                        cost = float(ingredient_cost) * ingredient_details['quantity_purchased']
                                        if converted_purchase_date.strftime('%B') == custom_month_for_profit:
                                            monthly_ingredient_cost += float(cost)

                                    print(f'Total expenses: RM {monthly_repair_cost + monthly_ingredient_cost:.2f}\n')

                                    net_profit = monthly_sales - (monthly_repair_cost + monthly_ingredient_cost)
                                    if net_profit < 0:
                                        print(f'Net profit: RM {net_profit:.2f} (deficit)')
                                    elif net_profit > 0:
                                        print(f'Net profit: RM {net_profit:.2f} (surplus)')
                                    else:
                                        print(f'Net profit: RM {net_profit:.2f} (break-even point)')

                                    try:
                                        profit_margin = (net_profit/monthly_sales) * 100
                                        print(f'Profit margin: {profit_margin:.2f}%\n')

                                        if profit_margin < 0:
                                            print(f'The bakery lost approximately RM {profit_margin/100:.2f} for every RM earned.')
                                            print('❗ The bakery might be facing financial struggles. Try to reduce costs and\n adjust pricing to prevent continued losses.')
                                        elif profit_margin > 0:
                                            print(f'The bakery make RM {profit_margin/100:.2f} for every RM earned.')
                                            print('🎊 Congrats! The business is healthy and sustainable.')
                                        else:
                                            print(f'The bakery is not making any profit.')
                                            print('A robust business strategy is needed to enhance the profitability in the future.')

                                        print('\n' + '-' * 85)

                                    except ZeroDivisionError:
                                        print('\n⚠️ The profit margin cannot be calculated as it has no income.')

                                else:
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid month. Please enter again. |')
                                    print('+--------------------------------------+')

                        except ValueError:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                else:
                    break
        elif track_choice == '4':
            print('\nExiting to Manager Privilege......')
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

