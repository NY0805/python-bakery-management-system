import json


# Function to load product discount information from file
def discount_management():
    try:
        file = open('product_discount.txt', 'r')  # open the file and read
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


# Function to save product data and discounts to the file
def save_discounts(discounts):
    with open('product_discount.txt', 'w') as file:
        json.dump(discounts, file, indent=4)


discounts = discount_management()


def validate_discount_input():
    while True:
        try:
            discount = float(input("Enter discount percentage (0-100): "))
            if 0 <= discount <= 100:  # Ensure discount input is within valid range
                return discount
            else:
                print("⚠️ Invalid input. Discount must be between 0 and 100.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid number.")


def add_discount():
    # Load existing products
    products = discount_management()

    product_code = input("Enter product code: ")

    # Check if the product code already exists
    for details in products.values():
        if details['product_code'] == product_code:
            print(f"Product code {product_code} already exists. Please use 'Modify Discount' to update the discount.")
            return  # Exit if product code exists

    product_name = input("Enter product name: ")

    # Validate stock input
    while True:
        stock_input = input("Enter product stock: ")
        if stock_input.isdigit():  # Check if the input to see is a digit or not
            stock = int(stock_input)
            break  # Break the loop if valid input
        else:
            print("Please enter a valid positive integer for stock.")

    # Validate price input
    while True:
        price_input = input("Enter product price: ")
        try:
            price = float(price_input)
            if price >= 0:  # Ensure price is non-negative
                break  # Break the loop if valid input
            else:
                print("Please enter a valid positive number for price.")
        except ValueError:
            print("Invalid input! Please enter numbers only.")

    # Validate discount input
    discount = validate_discount_input()

    # Create a new product entry
    new_entry_number = str(len(products) + 1)  # Increment the count for the new entry

    new_entry = {
        "Product Name": product_name,
        "product_code": product_code,
        "Stock": stock,
        "Price": f"RM {price:.2f}",
        "Discount": f"{discount}%"
    }

    # Add the new entry to the products dictionary
    products[new_entry_number] = new_entry

    save_discounts(products)

    print(f"New product {product_name} added with a discount of {discount} %.")


# Function to delete a discount (set to 0% or remove product)
def delete_discount():
    product_code = input("Enter product code: ")
    found = False

    for details in discounts.values():
        if details['product_code'] == product_code:
            found = True
            if details['Discount'] != "0%":
                details['Discount'] = "0%"
                save_discounts(discounts)
                print(f"Product {product_code}'s discount has been deleted and set to 0%.")
            else:
                print(f"|⚠️The discount for product {product_code} is already 0%, no changes made.|")
            break

    if not found:
        print(f"|⚠️No discount found for product {product_code}.|")


# Function to modify an existing discount
def modify_discount():
    product_code = input("Enter product code: ")
    found = False

    for details in discounts.values():
        if details['product_code'] == product_code:
            found = True
            new_discount = validate_discount_input()  # Use the validated input
            details['Discount'] = f"{new_discount}%"
            save_discounts(discounts)  # Save the updated discounts to the file
            print(f"Discount for product {product_code} updated to {new_discount}%.")
            break

    if not found:
        print(f"|⚠️No discount found for product {product_code}. Use 'Add Discount' to create a new discount.|")


# Function to print current product discount details
def display_discounts():
    print('\n -- Current Discounts and Product Details -- ')
    print('─' * 70)
    for product_number, product_info in discounts.items():
        product_name = product_info.get('Product Name', '').ljust(20)
        product_code_display = product_info.get('product_code', '').ljust(15)
        stock = str(product_info.get('Stock', 0)).ljust(10)
        price = product_info.get('Price', '').ljust(15)
        discount = product_info.get('Discount', '0%').ljust(15)
        print(f"{product_name}{product_code_display}{stock}{price}{discount}")

    print('-' * 70)


def manage_discounts():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'DISCOUNT MANAGEMENT')
        print('-----------------------------------------------')
        print("1. Add Discount")
        print("2. Modify Discount")
        print("3. Delete Discount")
        print("4. View All Discounts")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_discount()
        elif choice == '2':
            modify_discount()
        elif choice == '3':
            delete_discount()
        elif choice == '4':
            display_discounts()
        elif choice == '5':
            confirm_exit = input("Are you sure you want to exit? yes=y / no=n: ").lower()
            if confirm_exit == 'y':
                print("*** Exiting Discount Management. Goodbye! ***")
                break
            else:
                print("Returning to the menu.")
        else:
            print("|⚠️ Invalid option. Please try again.|")


#manage_discounts()
