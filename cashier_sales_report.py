import json
import random
from datetime import datetime


# Define the function that loads previous sales report data from the file
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


# Define the function that loads customer rating and reviews from the file
def load_data_from_customer_review():
    try:
        file = open('customer_reviews.txt', 'r')  # open the file and read
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


# Define the function that loads customer payment history from the file
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


# Define the function that saves generated sales report to the file
def save_info(sales_report):
    file = open('cashier_sales_report.txt', 'w')  # open the file to write
    json.dump(sales_report, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# validate and print error message when meet empty entries
def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...\n')
        return False


# print the title at the center for design purpose
def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


# store the data that retrieved from file into variable
cashier_transaction_keeping = load_data_from_cashier_transaction_keeping()
sales_report_file = load_data_from_sales_report()
customer_review = load_data_from_customer_review()


# define the function to generate sales performance report and product popularity report
def generate_sales_report():
    print('')
    printed_centered('SALES PERFORMANCE REPORT')  # display type of sales report user can generate
    print('1. Yearly report')
    print('2. Monthly report')
    print('3. Product popularity')
    print('4. Back to previous page')
    while True:
        # collect the choice of user and execute corresponding functions
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
                return False
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Please enter a valid index number. |')
                print('+--------------------------------------+')


# define the function to find out the available years for users to choose based on previous customer payment history
def allowable_year():
    allowable_years = set()
    for key, items in cashier_transaction_keeping.items():
        order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
        allowable_years.add(order_date.year)

    allowable_years_unpack = ', '.join(str(year) for year in list(allowable_years))

    return allowable_years_unpack


# define the function to find out the available months for users to choose based on previous customer payment history
def allowable_month(report_year):
    allowable_months = set()
    for key, items in cashier_transaction_keeping.items():
        order_date = datetime.strptime(items['order_date'], '%d-%m-%Y')
        if order_date.year == int(report_year):  # identify available months based on particular year selected by user
            allowable_months.add(order_date.month)

    allowable_month_unpack = ', '.join(str(month) for month in list(allowable_months))

    return allowable_month_unpack


# define the function to generate yearly sales report
def yearly_sales_performance():
    while True:
        while True:
            # generate a 4 digit unique report number for each report
            report_num = random.randint(1000, 9999)
            if report_num not in sales_report_file.keys():  # break when the generated report number is not duplicate
                break

        allowable_years = allowable_year()  # determine available years

        print(f'\nAllowable year: {allowable_years}')  # print available years

        report_year = input('Please enter the year you want to generate report: ')  # collect user selected year
        if validation_empty_entries(report_year):
            if report_year in allowable_years:  # check if selected year is in the list of valid years

                # initialize counter for sales and orders
                total_sales = 0
                total_orders = 0
                previous_total_sales = 0
                previous_total_orders = 0
                previous_year = int(report_year) - 1  # calculate the previous year for comparison

                # loop through customer payment history
                for key, item in cashier_transaction_keeping.items():
                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                    order_year = order_date.year
                    if order_year == int(report_year):  # if met the same year as the selected year
                        total_sales += float(item['total_spend(RM)'])  # add the total spend
                        total_orders += 1  # add 1 to calculate the total orders
                    if order_year == previous_year:  # for the previous year
                        previous_total_sales += float(item['total_spend(RM)'])  # add the total spend
                        previous_total_orders += 1  # add 1 to calculate the total orders

                # calculate sales growth and percentage difference if there were sales in both years
                if total_sales and previous_total_sales != 0:
                    sales_ratio = (total_sales / previous_total_sales) * 100
                    percentage_difference = ((total_sales - previous_total_sales) / previous_total_sales) * 100
                    formatted_sales_ratio = f"{sales_ratio:.2f}%"
                    formatted_percentage_difference = f"{percentage_difference:.2f}%"
                else:
                    # predefined display message if no previous data exists
                    formatted_sales_ratio = 'No previous sales.'
                    formatted_percentage_difference = 'No previous sales.'

                # display the yearly performance summary
                print('\n----------------------------------------------------------')
                print(f"\t\t\t{report_year}'S YEARLY PERFORMANCE SUMMARY")
                print('----------------------------------------------------------')
                print(f'{"Total Sales":<13}: {total_sales:.2f}')
                print(f'{"Total Orders":<13}: {total_orders}')
                print('')
                print(f'Sales Growth(%) for {report_year} Compared to {previous_year:<5}: {formatted_sales_ratio}')
                print(f'{"Actual Percentage Growth":<42}: {formatted_percentage_difference}')
                break
            else:
                # display error message if year input is invalid
                print('\n+-------------------------------------+')
                print('|⚠️ Please enter based on given year. |')
                print('+-------------------------------------+')

    while True:
        # collect user input whether to save the report
        save_report = input('\nSave this report to system? (y=yes, n=no): ').lower().strip()
        if validation_empty_entries(save_report):
            if save_report == 'y':  # if choose to save
                report_exist = False
                for key, value in sales_report_file.items():
                    # check for existing report for the same year and type
                    if value['report_type'] == 'yearly sales report' and report_year == value['selected_year']:
                        print('\n+--------------------------------------------------------------------------------+')
                        print('|⚠️ The report cannot be saved because the same report has been saved previously.|')
                        print('+--------------------------------------------------------------------------------+')
                        report_exist = True

                if not report_exist:  # if no duplicate report, save the report
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

            elif save_report == 'n':  # if choose not to save report
                print('Exit to previous page......')
                break
            else:
                # print error message when input is invalid
                print('\n+------------------------+')
                print('|⚠️ Please enter y or n. |')
                print('+------------------------+')

    while True:
        # collect user input whether to generate another yearly report
        generate_more = input('\nContinue generating yearly sales report? (y=yes, n=no)\n'
                              '>>> ').lower().strip()
        if validation_empty_entries(generate_more):
            if generate_more == 'y':  # if yes
                yearly_sales_performance()  # call the function again
                break
            elif generate_more == 'n':  # if no
                print('\nExit the yearly performance report page......')
                generate_sales_report()  # return to the main sales report page
                break
            else:
                # print error message when input is invalid
                print('\n+------------------------+')
                print('|⚠️ Please enter y or n. |')
                print('+------------------------+')


# define function to generate monthly sales report
def monthly_sales_performance():
    while True:
        while True:
            # generate a 4 digit unique report number for each report
            report_num = random.randint(1000, 9999)
            if report_num not in sales_report_file.keys():  # break when the generated report number is not duplicate
                break

        allowable_years = allowable_year()  # determine available years

        print(f'\nAllowable year: {allowable_years}')

        # collect user selected year
        report_year = input('Please enter the year you want to generate report: ')
        if validation_empty_entries(report_year):
            if report_year in allowable_years:  # check if selected year is in the list of valid years
                break
            else:
                print('\n+--------------------------------------------------+')
                print('|⚠️ Please enter a valid year based on given year. |')
                print('+--------------------------------------------------+')

    while True:
        allowable_months = allowable_month(report_year)  # determine available months

        print(f'\nAllowable month: {allowable_months}')

        # collect user selected month
        report_month = input('Please enter the month you want to generate report: ')
        if validation_empty_entries(report_month):
            if report_month in allowable_months:  # check if selected month is in the list of valid months

                # initialize counter for sales and orders
                total_sales = 0
                total_orders = 0
                previous_total_sales = 0
                previous_total_orders = 0
                if int(report_month) != 1:
                    previous_month = int(report_month) - 1  # calculate previous month for comparison
                else:
                    previous_month = int(report_month)  # no previous month if the selected month is January

                # loop through customer payment history
                for key, item in cashier_transaction_keeping.items():
                    order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
                    order_year = order_date.year
                    order_month = order_date.month

                    if order_year == int(report_year):  # if met the same year as the selected year
                        if order_month == int(report_month):  # if met the same month as the selected month
                            total_sales += float(item['total_spend(RM)'])  # add the total spend
                            total_orders += 1  # add 1 to calculate total orders
                        if order_month == previous_month:  # if previous month
                            previous_total_sales += float(item['total_spend(RM)'])  # add the total spend
                            previous_total_orders += 1  # add 1 to calculate total orders

                # calculate the sales growth and percentage difference if there were sales in both month
                if total_sales and previous_total_sales != 0:
                    sales_ratio = (total_sales / previous_total_sales) * 100
                    percentage_difference = ((total_sales - previous_total_sales) / previous_total_sales) * 100
                    formatted_sales_ratio = f"{sales_ratio:.2f}%"
                    formatted_percentage_difference = f"{percentage_difference:.2f}%"
                else:
                    # predefined display message if no previous sales data exists
                    formatted_sales_ratio = 'No previous sales'
                    formatted_percentage_difference = 'No previous sales'

                # display the monthly performance summary
                print('\n----------------------------------------------------------')
                print(f"\t\t\t{report_month}/{report_year} SALES PERFORMANCE SUMMARY")
                print('----------------------------------------------------------')
                print(f'{"Total Sales":<15}: {total_sales:.2f}')
                print(f'{"Total Orders":<15}: {total_orders}')
                print('')
                print(
                    f'Sales Growth for {report_month}/{report_year} Compared to {previous_month}/{report_year:<5}: {formatted_sales_ratio}')
                print(f'{"Actual Percentage Growth":<44}: {formatted_percentage_difference}')
                break
            else:
                # print error message if input is invalid
                print('\n+--------------------------------------+')
                print('|⚠️ Please enter based on given month. |')
                print('+--------------------------------------+')

    while True:
        # collect user input whether to save the generated report
        save_report = input('\nSave this report to system? (y=yes, n=no): ').lower().strip()
        if validation_empty_entries(save_report):
            if save_report == 'y':  # if choose to save
                report_exist = False
                for key, value in sales_report_file.items():
                    # check for existing report for the same year, month and type
                    if value['report_type'] == 'monthly sales report' and report_year == value['selected_year'] and report_month == value['selected_month']:
                        print('\n+--------------------------------------------------------------------------------+')
                        print('|⚠️ The report cannot be saved because the same report has been saved previously.|')
                        print('+--------------------------------------------------------------------------------+')
                        report_exist = True

                # if no duplicate, save report
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
            elif save_report == 'n':  # if choose not to save
                print('Exit to previous page.')
                break
            else:
                # print error message when input is invalid
                print('\n+-----------------------+')
                print('|⚠️ Please enter y or n.|')
                print('+-----------------------+')

    while True:
        # collect user input whether to generate another monthly sales report
        generate_more = input('\nContinue generating monthly sales report? (y=yes, n=no)\n'
                              '>>> ').lower().strip()
        if validation_empty_entries(generate_more):
            if generate_more == 'y':  # if yes
                monthly_sales_performance()  # call the function again
                break
            elif generate_more == 'n':  # if no
                print('\nExit the yearly performance report page......')
                generate_sales_report()  # return to the main sales report
                break
            else:
                # print error message when user input is invalid
                print('\n+-----------------------+')
                print('|⚠️ Please enter y or n.|')
                print('+-----------------------+')


# define the function to calculate the product popularity based on users option
def product_popularity_customer_review(report_year, report_month, best_seller, least_seller, all):
    # initialize variables to store ratings and reviews for best and least seller product
    best_rating = 0
    best_count = 0
    best_review = {}
    least_rating = 0
    least_count = 0
    least_review = {}

    # loop through customer reviews
    for key, item in customer_review.items():
        # extract the year and month of each review
        order_date = datetime.strptime(item['order_date'], '%d-%m-%Y')
        order_year = order_date.year
        order_month = order_date.month

        # if user choose to generate overall product popularity report
        if all:
            # calculate the sum of rating and add the corresponding reviews to best_review dictionary
            if best_seller in item['product_name']:
                best_rating += item['rating']
                best_count += 1
                best_review[item['username']] = item['review']
            # calculate the sum of rating and add the corresponding reviews to least_review dictionary
            if least_seller in item['product_name']:
                least_rating += item['rating']
                least_count += 1
                least_review[item['username']] = item['review']

        # if user choose to generate yearly product popularity report
        elif best_seller in item['product_name'] and order_year == int(report_year):  # filter the result by user selected year and best seller product
            if report_month is None:
                best_rating += item['rating']
                best_count += 1
                best_review[item['username']] = item['review']
            else:
                # if user choose to generate monthly product popularity report
                if order_month == int(report_month):  # filter the result by user selected year, month and best seller product
                    best_rating += item['rating']
                    best_count += 1
                    best_review[item['username']] = item['review']

        # same as the bestseller product
        elif least_seller in item['product_name'] and order_year == int(report_year):
            if report_month is None:
                least_rating += item['rating']
                least_count += 1
                least_review[item['username']] = item['review']
            else:
                if order_month == int(report_month):
                    least_rating += item['rating']
                    least_count += 1
                    least_review[item['username']] = item['review']

    # when bestseller and least seller is the same product
    if best_seller == least_seller:
        least_rating = best_rating
        least_count = best_count
        least_review = best_review

    # when there are ratings for the bestseller and least seller product
    if best_count > 0:
        # calculate the average rating and select a random review with the corresponding username
        best_average_rating = best_rating / best_count
        best_random_customer = random.choice(list(best_review.keys()))
        best_random_review = best_review[best_random_customer]
    else:
        # predefined display message when there is no rating
        best_random_customer = None
        best_average_rating = 'No rating detected.'
        best_random_review = 'No review detected.'

    if least_count > 0:
        # calculate the average rating and select a random review with the corresponding username
        least_average_rating = least_rating / least_count
        least_random_customer = random.choice(list(least_review.keys()))
        least_random_review = least_review[least_random_customer]
    else:
        # predefined display message when there is no rating
        least_random_customer = None
        least_average_rating = 'No rating detected.'
        least_random_review = 'No review detected.'

    return best_average_rating, best_random_customer, best_random_review, least_average_rating, least_random_customer, least_random_review, best_count, least_count


# define the function to calculate and display product popularity based on user option
def product_popularity():
    while True:
        while True:
            # display option for report type
            print('')
            printed_centered('PRODUCT POPULARITY')
            print('1. Yearly report')
            print('2. Monthly report')
            print('3. Overall product popularity summary')
            print('4. Back to previous page')
            report_service = input('\nPlease input the index number of the service you choose: ')
            if validation_empty_entries(report_service):

                # if user choose to generate yearly report
                if report_service == '1':
                    allowable_years = allowable_year()

                    print(f'\nAllowable year: {allowable_years}')

                    report_year = input('Please enter the year you want to generate report: ')
                    if validation_empty_entries(report_year):
                        if report_year in allowable_years:  # ensure the input is within available years
                            product_ordered = {}
                            # calculate quantity sold for each product in the selected year
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

                            # initialize counter
                            best_seller = None
                            least_seller = None
                            max_quantity = -1
                            min_quantity = float('inf')

                            # if there are product detected in the selected year
                            if product_ordered:
                                # identify bestseller, least seller and their corresponding quantity sold
                                for name, quantity in product_ordered.items():
                                    if quantity > max_quantity:
                                        max_quantity = quantity
                                        best_seller = name

                                    if quantity < min_quantity:
                                        min_quantity = quantity
                                        least_seller = name

                            # predefined message f there are no product detected
                            else:
                                best_seller = 'No products sold'
                                max_quantity = 0
                                least_seller = 'No products sold'
                                min_quantity = 0

                            # get customer rating and review
                            best_average_rating, best_random_customer, best_random_review, least_average_rating, least_random_customer, least_random_review, best_count, least_count = product_popularity_customer_review(
                                report_year, None, best_seller, least_seller, all=False)

                            # print the summary for yearly report
                            print('\n----------------------------------------------------------')
                            print(f"\t\t\t{report_year}'S PRODUCT POPULARITY SUMMARY")
                            print('----------------------------------------------------------')
                            print(f'\n{"1️⃣ Top-selling product":<31}: {best_seller.title()}')
                            print(f'{"📌 Total quantity sold":<29}: {max_quantity}')
                            print(f'{"⭐ Average customer rating":<29}: {best_average_rating}')
                            if best_count > 0:
                                print(
                                    f'{"🎉 Customer review spotlight":<29}: "{best_random_review}" ----- {best_random_customer}')
                            else:
                                print(f'{"🎉 Customer review spotlight":<29}: {best_random_review}')

                            print(f'\n{"↘️ Least-selling product":<30}: {least_seller.title()}')
                            print(f'{"📌 Total quantity sold":<29}: {min_quantity}')
                            print(f'{"⭐ Average customer rating":<29}: {least_average_rating}')
                            if least_count > 0:
                                print(
                                    f'{"🎉 Customer review spotlight":<29}: "{least_random_review}" ----- {least_random_customer}')
                            else:
                                print(f'{"🎉 Customer review spotlight":<29}: {least_random_review}')
                            break
                        else:
                            print('\n+-------------------------------------------------+')
                            print('|⚠️ Please enter a valid year based on given year.|')
                            print('+-------------------------------------------------+')
                            break

                # if user choose to generate monthly product popularity report
                elif report_service == '2':
                    while True:
                        allowable_years = allowable_year()

                        print(f'\nAllowable year: {allowable_years}')

                        # collect user selected year and ensure it is within the available years
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

                        # collect user selected month and ensure it is within the available month
                        report_month = input('Please enter the month you want to generate report: ')
                        if validation_empty_entries(report_month):
                            if report_month in allowable_months:
                                product_ordered = {}
                                # calculate quantity sold for each product in the selected year and month
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

                                # initialize counter
                                best_seller = None
                                least_seller = None
                                max_quantity = -1
                                min_quantity = float('inf')

                                # if there are product detected in the selected year and month
                                if product_ordered:
                                    # identify bestseller, least seller and their corresponding quantity sold
                                    for name, quantity in product_ordered.items():
                                        if quantity > max_quantity:
                                            max_quantity = quantity
                                            best_seller = name

                                        if quantity < min_quantity:
                                            min_quantity = quantity
                                            least_seller = name
                                else:
                                    # predefined message when no product detected
                                    best_seller = 'No products sold'
                                    max_quantity = 0
                                    least_seller = 'No products sold'
                                    min_quantity = 0

                                # get the customer average ratings and review
                                best_average_rating, best_random_customer, best_random_review, least_average_rating, least_random_customer, least_random_review, best_count, least_count = product_popularity_customer_review(
                                    report_year, report_month, best_seller, least_seller, all=False)

                                # print the summary of monthly report
                                print('\n----------------------------------------------------------')
                                print(f"\t\t\t{report_month}/{report_year} PRODUCT POPULARITY SUMMARY")
                                print('----------------------------------------------------------')
                                print(f'\n{"1️⃣ Top-selling product":<31}: {best_seller.title()}')
                                print(f'{"📌 Total quantity sold":<29}: {max_quantity}')
                                print(f'{"⭐ Average customer rating":<29}: {best_average_rating}')
                                if best_count > 0:
                                    print(
                                        f'{"🎉 Customer review spotlight":<29}: "{best_random_review}" ----- {best_random_customer}')
                                else:
                                    print(f'{"🎉 Customer review spotlight":<29}: {best_random_review}')

                                print(f'\n{"↘️ Least-selling product":<30}: {least_seller.title()}')
                                print(f'{"📌 Total quantity sold":<29}: {min_quantity}')
                                print(f'{"⭐ Average customer rating":<29}: {least_average_rating}')
                                if least_count > 0:
                                    print(
                                        f'{"🎉 Customer review spotlight":<29}: "{least_random_review}" ----- {least_random_customer}')
                                else:
                                    print(f'{"🎉 Customer review spotlight":<29}: {least_random_review}')
                                break
                            else:
                                print('\n+--------------------------------------+')
                                print('|⚠️ Please enter based on given month. |')
                                print('+--------------------------------------+')
                                break

                # if user choose to generate overall product popularity report
                elif report_service == '3':
                    product_ordered = {}
                    # calculate quantity sold for each product in the selected year and month
                    for key, item in cashier_transaction_keeping.items():
                        for product in item['items']:
                            total_product = product.split(' x ')
                            if total_product[0] in product_ordered:
                                product_ordered[total_product[0]] += int(total_product[1])
                            else:
                                product_ordered[total_product[0]] = int(total_product[1])

                    # initialize counter
                    best_seller = None
                    least_seller = None
                    max_quantity = -1
                    min_quantity = float('inf')

                    # if there are product detected
                    if product_ordered:
                        # identify bestseller, least seller and their corresponding quantity sold
                        for name, quantity in product_ordered.items():
                            if quantity > max_quantity:
                                max_quantity = quantity
                                best_seller = name

                            if quantity < min_quantity:
                                min_quantity = quantity
                                least_seller = name
                    else:
                        # predefined message if no product detected
                        best_seller = 'No products sold'
                        max_quantity = 0
                        least_seller = 'No products sold'
                        min_quantity = 0

                    # get customer average rating and review
                    best_average_rating, best_random_customer, best_random_review, least_average_rating, least_random_customer, least_random_review, best_count, least_count = product_popularity_customer_review(
                        None, None, best_seller, least_seller, all=True)

                    # print the summary of overall product popularity report
                    print('\n----------------------------------------------------------')
                    print(f"\t\t\tOVERALL PRODUCT POPULARITY SUMMARY")
                    print('----------------------------------------------------------')
                    print(f'\n{"1️⃣ Top-selling product":<31}: {best_seller.title()}')
                    print(f'{"📌 Total quantity sold":<29}: {max_quantity}')
                    print(f'{"⭐ Average customer rating":<29}: {best_average_rating}')
                    if best_count > 0:
                        print(
                            f'{"🎉 Customer review spotlight":<29}: "{best_random_review}" ----- {best_random_customer}')
                    else:
                        print(f'{"🎉 Customer review spotlight":<29}: {best_random_review}')

                    print(f'\n{"↘️ Least-selling product":<30}: {least_seller.title()}')
                    print(f'{"📌 Total quantity sold":<29}: {min_quantity}')
                    print(f'{"⭐ Average customer rating":<29}: {least_average_rating}')
                    if least_count > 0:
                        print(
                            f'{"🎉 Customer review spotlight":<29}: "{least_random_review}" ----- {least_random_customer}')
                    else:
                        print(f'{"🎉 Customer review spotlight":<29}: {least_random_review}')
                    break

                # if user choose to back to previous page
                elif report_service == '4':
                    generate_sales_report()  # return to main sales report page
                    break
                else:
                    # print error message when input is invalid
                    print('\n+-------------------------------------+')
                    print('|⚠️ Please enter a valid index number.|')
                    print('+-------------------------------------+')



