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


def load_data_from_customer_order_list():
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


sales_list = load_data_from_customer_order_list()
sales_report_file = load_data_from_sales_report()


def generate_sales_report():
    print('\nWelcome to sales report page.')
    print('1. yearly report')
    print('2. monthly report')
    report_service = input('choose: ')
    if report_service == '1':
        yearly_sales_performance()
    elif report_service == '2':
        monthly_sales_performance()


def yearly_sales_performance():
    while True:
        while True:
            report_num = random.randint(1000,9999)
            if report_num not in sales_list.keys():
                break

        allowable_years = set()
        for key, items in sales_list.items():
            order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
            allowable_years.add(order_date.year)

        allowable_years_unpack = ', '.join(str(year) for year in list(allowable_years))

        print(f'\nAllowable year: {allowable_years_unpack}')

        report_year = input('Please enter the year you want to generate report: ')
        if validation_empty_entries(report_year):
            if report_year in allowable_years_unpack:
                total_sales = 0
                total_orders = 0
                for key, item in sales_list.items():
                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                    order_year = order_date.year
                    if order_year == int(report_year):
                        if item['status'] == 'Payment Completed':
                            total_sales += item['total_price (RM)']
                            total_orders += 1
                print(f'total sales: {total_sales}')
                print(f'total orders: {total_orders}')
                break
            else:
                print('please enter based on given year')

    while True:
        save_report = input('Save this report to system? (y=yes, n=no): ')
        if save_report == 'y':
            sales_report_file[report_num] = {
                'report_type': 'yearly sales report',
                'selected_year': report_year,
                'total_sales': total_sales,
                'total_order': total_orders
            }
            save_info(sales_report_file)
            break
        elif save_report == 'n':
            print('\nexit to previous page.')
            generate_sales_report()
            break
        else:
            print('please enter y or n.')



def monthly_sales_performance():
    while True:
        while True:
            report_num = random.randint(1000, 9999)
            if report_num not in sales_list.keys():
                break
        allowable_years = set()
        for key, items in sales_list.items():
            order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
            allowable_years.add(order_date.year)

        allowable_years_unpack = ', '.join(str(year) for year in list(allowable_years))

        print(f'\nAllowable year: {allowable_years_unpack}')

        report_year = input('Please enter the year you want to generate report: ')
        if validation_empty_entries(report_year):
            if int(report_year) in allowable_years:
                break
            else:
                print('please enter a valid year based on given year.')

    while True:
        allowable_month = set()
        for key, items in sales_list.items():
            order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
            allowable_month.add(order_date.month)

        allowable_month_unpack = ', '.join(str(month) for month in list(allowable_month))

        print(f'\nAllowable month: {allowable_month_unpack}')

        report_month = input('Please enter the month you want to generate report: ')
        if validation_empty_entries(report_month):
            if int(report_month) in allowable_month:
                total_sales = 0
                total_orders = 0
                for key, item in sales_list.items():
                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                    order_year = order_date.year
                    order_month = order_date.month

                    if order_year == int(report_year):
                        if order_month == int(report_month):
                            if item['status'] == 'Payment Completed':
                                total_sales += item['total_price (RM)']
                                total_orders += 1
                print(f'total sales: {total_sales}')
                print(f'total orders: {total_orders}')
                break
            else:
                print('please enter based on given month')

    while True:
        save_report = input('Save this report to system? (y=yes, n=no): ')
        if save_report == 'y':
            sales_report_file[report_num] = {
                'report_type': 'monthly sales report',
                'selected_year': report_year,
                'selected_month': report_month,
                'total_sales': total_sales,
                'total_order': total_orders
            }
            save_info(sales_report_file)
            break
        elif save_report == 'n':
            print('\nexit to previous page.')
            generate_sales_report()
            break
        else:
            print('please enter y or n.')


#generate_sales_report()
