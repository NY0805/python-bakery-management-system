import json
import random
from datetime import datetime


def load_data_from_sales_report():
    try:
        file = open('cashier_sales_report.txt', 'r')  # open the file and read
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


def save_info(sales_report):
    file = open('cashier_sales_report.txt', 'w')  # open the file to write
    json.dump(sales_report, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...\n')
        return False


cashier_transaction_keeping = load_data_from_cashier_transaction_keeping()
sales_report_file = load_data_from_sales_report()


def generate_sales_report():
    print('Welcome to sales performance page.')
    print('1. Yearly report')
    print('2. Monthly report')
    print('3. Product popularity')
    print('4. Back to previous page')
    while True:
        report_service = input('\nPlease input the index number of the service you choose: ')
        if validation_empty_entries(report_service):
            if report_service == '1':
                yearly_sales_performance()
                break
            elif report_service == '2':
                monthly_sales_performance()
                break
            elif report_service == '3':
                product_popularity()
                break
            elif report_service == '4':
                pass
            else:
                print('\n+-------------------------------------+')
                print('|⚠️ Please enter a valid index number |')
                print('+-------------------------------------+')


def allowable_year():
    allowable_years = set()
    for key, items in cashier_transaction_keeping.items():
        order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
        allowable_years.add(order_date.year)

    allowable_years_unpack = ', '.join(str(year) for year in list(allowable_years))

    return allowable_years_unpack


def allowable_month(report_year):
    allowable_months = set()
    for key, items in cashier_transaction_keeping.items():
        order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
        if order_date.year == int(report_year):
            allowable_months.add(order_date.month)

    allowable_month_unpack = ', '.join(str(month) for month in list(allowable_months))

    return allowable_month_unpack


def yearly_sales_performance():
    while True:
        while True:
            report_num = random.randint(1000, 9999)
            if report_num not in sales_report_file.keys():
                break

        allowable_years = allowable_year()

        print(f'\nAllowable year: {allowable_years}')

        report_year = input('Please enter the year you want to generate report: ')
        if validation_empty_entries(report_year):
            if report_year in allowable_years:
                total_sales = 0
                total_orders = 0
                for key, item in cashier_transaction_keeping.items():
                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                    order_year = order_date.year
                    if order_year == int(report_year):
                        total_sales += float(item['total_spend(RM)'])
                        total_orders += 1
                print('\n----------------------------------------------------------')
                print(f"\t\t\t{report_year}'S YEARLY PERFORMANCE SUMMARY")
                print('----------------------------------------------------------')
                print(f'Total sales: {total_sales}')
                print(f'Total orders: {total_orders}')
                break
            else:
                print('\n+-------------------------------------+')
                print('|⚠️ Please enter based on given year. |')
                print('+-------------------------------------+')

    while True:
        save_report = input('\nSave this report to system? (y=yes, n=no): ').lower().strip()
        if validation_empty_entries(save_report):
            if save_report == 'y':
                report_exist = False
                for key, value in sales_report_file.items():
                    if value['report_type'] == 'yearly sales report' and report_year == value['selected_year']:
                        print('\n+--------------------------------------------------------------------------------+')
                        print('|⚠️ The report cannot be saved because the same report has been saved previously.|')
                        print('+--------------------------------------------------------------------------------+')

                        report_exist = True

                if not report_exist:
                    sales_report_file[report_num] = {
                        'report_type': 'yearly sales report',
                        'selected_year': report_year,
                        'total_sales': total_sales,
                        'total_order': total_orders
                    }
                    save_info(sales_report_file)
                    print('\n+---------------------+')
                    print('| Successfully saved! |')
                    print('+---------------------+')

                    break
                break
            elif save_report == 'n':
                print('Exit to previous page......')
                break
            else:
                print('\n+------------------------+')
                print('|⚠️ Please enter y or n. |')
                print('+------------------------+')

    while True:
        generate_more = input('\nContinue generating yearly sales report? (y=yes, n=no)\n'
                              '>>> ').lower().strip()
        if validation_empty_entries(generate_more):
            if generate_more == 'y':
                yearly_sales_performance()
                break
            elif generate_more == 'n':
                print('\nExit the yearly performance report page......')
                generate_sales_report()
                break
            else:
                print('\n+------------------------+')
                print('|⚠️ Please enter y or n. |')
                print('+------------------------+')


def monthly_sales_performance():
    while True:
        while True:
            report_num = random.randint(1000, 9999)
            if report_num not in sales_report_file.keys():
                break

        allowable_years = allowable_year()

        print(f'\nAllowable year: {allowable_years}')

        report_year = input('Please enter the year you want to generate report: ')
        if validation_empty_entries(report_year):
            if report_year in allowable_years:
                break
            else:
                print('\n+--------------------------------------------------+')
                print('|⚠️ Please enter a valid year based on given year. |')
                print('+--------------------------------------------------+')

    while True:
        allowable_months = allowable_month(report_year)

        print(f'\nAllowable month: {allowable_months}')

        report_month = input('Please enter the month you want to generate report: ')
        if validation_empty_entries(report_month):
            if report_month in allowable_months:
                total_sales = 0
                total_orders = 0
                for key, item in cashier_transaction_keeping.items():
                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                    order_year = order_date.year
                    order_month = order_date.month

                    if order_year == int(report_year):
                        if order_month == int(report_month):
                            total_sales += float(item['total_spend(RM)'])
                            total_orders += 1
                print('\n----------------------------------------------------------')
                print(f"\t\t\t{report_month}/{report_year} SALES PERFORMANCE SUMMARY")
                print('----------------------------------------------------------')
                print(f'total sales: {total_sales}')
                print(f'total orders: {total_orders}')
                break
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Please enter based on given month. |')
                print('+--------------------------------------+')

    while True:
        save_report = input('\nSave this report to system? (y=yes, n=no): ').lower().strip()
        if validation_empty_entries(save_report):
            if save_report == 'y':
                report_exist = False
                for key, value in sales_report_file.items():
                    if value['report_type'] == 'monthly sales report' and report_year == value[
                        'selected_year'] and report_month == value['selected_month']:
                        print('\n+--------------------------------------------------------------------------------+')
                        print('|⚠️ The report cannot be saved because the same report has been saved previously.|')
                        print('+--------------------------------------------------------------------------------+')
                        report_exist = True

                if not report_exist:
                    sales_report_file[report_num] = {
                        'report_type': 'monthly sales report',
                        'selected_year': report_year,
                        'selected_month': report_month,
                        'total_sales': total_sales,
                        'total_order': total_orders
                    }
                    save_info(sales_report_file)
                    print('Successfully saved!')
                    break
                break
            elif save_report == 'n':
                print('Exit to previous page.')
                break
            else:
                print('\n+-----------------------+')
                print('|⚠️ Please enter y or n.|')
                print('+-----------------------+')

    while True:
        generate_more = input('\nContinue generating monthly sales report? (y=yes, n=no)\n'
                              '>>> ').lower().strip()
        if validation_empty_entries(generate_more):
            if generate_more == 'y':
                monthly_sales_performance()
                break
            elif generate_more == 'n':
                print('\nExit the yearly performance report page......')
                generate_sales_report()
                break
            else:
                print('\n+-----------------------+')
                print('|⚠️ Please enter y or n.|')
                print('+-----------------------+')


def product_popularity():
    while True:
        while True:
            report_num = random.randint(1000, 9999)
            if report_num not in sales_report_file.keys():
                break

        while True:
            print('Welcome to product popularity page!')
            print('1. Yearly report')
            print('2. Monthly report')
            print('3. Overall product popularity summary')
            print('4. Back to previous page')
            report_service = input('\nPlease input the index number of the service you choose: ')
            if validation_empty_entries(report_service):
                if report_service == '1':
                    allowable_years = allowable_year()

                    print(f'\nAllowable year: {allowable_years}')

                    report_year = input('Please enter the year you want to generate report: ')
                    if validation_empty_entries(report_year):
                        if report_year in allowable_years:
                            product_ordered = {}
                            for key, item in cashier_transaction_keeping.items():
                                order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                                order_year = order_date.year
                                if order_year == int(report_year):
                                    for product in item['items']:
                                        total_product = product.split(' x ')
                                        if total_product[0] in product_ordered:
                                            product_ordered[total_product[0]] += int(total_product[1])
                                        else:
                                            product_ordered[total_product[0]] = int(total_product[1])
                                    print(product_ordered)

                            best_seller = None
                            least_seller = None
                            max_quantity = -1
                            min_quantity = float('inf')

                            if product_ordered:
                                for name, quantity in product_ordered.items():
                                    if quantity > max_quantity:
                                        max_quantity = quantity
                                        best_seller = name

                                    if quantity < min_quantity:
                                        min_quantity = quantity
                                        least_seller = name

                            else:
                                best_seller = 'No products sold'
                                max_quantity = 0
                                least_seller = 'No products sold'
                                min_quantity = 0

                            print('\n----------------------------------------------------------')
                            print(f"\t\t\t{report_year}'S PRODUCT POPULARITY SUMMARY")
                            print('----------------------------------------------------------')
                            print(f'\nTop-selling product: {best_seller}, Total quantity sold: {max_quantity}')
                            print(f'Least-selling product: {least_seller}, Total quantity sold: {min_quantity}\n')
                            break
                        else:
                            print('\n+-------------------------------------------------+')
                            print('|⚠️ Please enter a valid year based on given year.|')
                            print('+-------------------------------------------------+')
                            break

                elif report_service == '2':
                    while True:
                        allowable_years = allowable_year()

                        print(f'\nAllowable year: {allowable_years}')

                        report_year = input('Please enter the year you want to generate report: ')
                        if validation_empty_entries(report_year):
                            if report_year in allowable_years:
                                break
                            else:
                                print('\n+-------------------------------------------------+')
                                print('|⚠️ Please enter a valid year based on given year.|')
                                print('+-------------------------------------------------+')

                    while True:
                        allowable_months = allowable_month(report_year)

                        print(f'\nAllowable month: {allowable_months}')

                        report_month = input('Please enter the month you want to generate report: ')
                        if validation_empty_entries(report_month):
                            if report_month in allowable_months:
                                product_ordered = {}
                                for key, item in cashier_transaction_keeping.items():
                                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                                    order_year = order_date.year
                                    order_month = order_date.month
                                    if order_year == int(report_year) and order_month == int(report_month):
                                        for product in item['items']:
                                            total_product = product.split(' x ')
                                            if total_product[0] in product_ordered:
                                                product_ordered[total_product[0]] += int(total_product[1])
                                            else:
                                                product_ordered[total_product[0]] = int(total_product[1])
                                        print(product_ordered)

                                best_seller = None
                                least_seller = None
                                max_quantity = -1
                                min_quantity = float('inf')

                                if product_ordered:
                                    for name, quantity in product_ordered.items():
                                        if quantity > max_quantity:
                                            max_quantity = quantity
                                            best_seller = name

                                        if quantity < min_quantity:
                                            min_quantity = quantity
                                            least_seller = name
                                else:
                                    best_seller = 'No products sold'
                                    max_quantity = 0
                                    least_seller = 'No products sold'
                                    min_quantity = 0

                                print('\n----------------------------------------------------------')
                                print(f"\t\t\t{report_month}/{report_year} PRODUCT POPULARITY SUMMARY")
                                print('----------------------------------------------------------')
                                print(f'\n{"Top-selling product":<25}: {best_seller}, Total quantity sold: {max_quantity}')
                                print(f'{"Least-selling product":<25}: {least_seller}, Total quantity sold: {min_quantity}\n')
                                break
                            else:
                                print('\n+--------------------------------------+')
                                print('|⚠️ Please enter based on given month. |')
                                print('+--------------------------------------+')
                                break
                elif report_service == '3':
                    product_ordered = {}
                    for key, item in cashier_transaction_keeping.items():
                        for product in item['items']:
                            total_product = product.split(' x ')
                            if total_product[0] in product_ordered:
                                product_ordered[total_product[0]] += int(total_product[1])
                            else:
                                product_ordered[total_product[0]] = int(total_product[1])
                        print(product_ordered)

                    best_seller = None
                    least_seller = None
                    max_quantity = -1
                    min_quantity = float('inf')

                    if product_ordered:
                        for name, quantity in product_ordered.items():
                            if quantity > max_quantity:
                                max_quantity = quantity
                                best_seller = name

                            if quantity < min_quantity:
                                min_quantity = quantity
                                least_seller = name
                    else:
                        best_seller = 'No products sold'
                        max_quantity = 0
                        least_seller = 'No products sold'
                        min_quantity = 0

                    print('\n----------------------------------------------------------')
                    print(f"\t\t\tOVERALL PRODUCT POPULARITY SUMMARY")
                    print('----------------------------------------------------------')
                    print(f'\n{"Top-selling product":<25}: {best_seller}, Total quantity sold: {max_quantity}')
                    print(f'{"Least-selling product":<25}: {least_seller}, Total quantity sold: {min_quantity}\n')
                    break
                    break
                elif report_service == '4':
                    generate_sales_report()
                    break
                else:
                    print('\n+-------------------------------------+')
                    print('|⚠️ Please enter a valid index number.|')
                    print('+-------------------------------------+')


generate_sales_report()
#product_popularity()
