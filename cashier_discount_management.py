import json


def load_cashier_discount_management():
    try:
        file = open('baker_product_keeping.txt', 'r')  # open the file and read
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


# A dictionary to store discounts. Product code is the key, discount is the value.
discounts = {}


# Function to add a discount
def add_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        print(f"Discount already exists for product {product_code}. Use 'modify' to update it.")
    else:
        discount = float(input("Enter discount percentage: "))
        discounts[product_code] = discount
        print(f"Discount of {discount}% added to product {product_code}.")


# Function to delete a discount
def delete_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        del discounts[product_code]
        print(f"Discount for product {product_code} has been removed.")
    else:
        print(f"No discount found for product {product_code}.")


# Function to modify an existing discount
def modify_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        new_discount = float(input("Enter new discount percentage: "))
        discounts[product_code] = new_discount
        print(f"Discount for product {product_code} updated to {new_discount}%.")
    else:
        print(f"No discount found for product {product_code}. Use 'add' to create a new discount.")


# Display all discounts
def display_discounts():
    if discounts:
        print("Current Discounts:")
        for product, discount in discounts.items():
            print(f"Product {product}: {discount}% off")
    else:
        print("No discounts available.")


# Let user to choose an option
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
                print("Exiting Discount Management.")
                break
            else:
                print("Returning to the menu.")
        else:
            print("|⚠️Invalid option. Please try again.|")


# Call the main function

