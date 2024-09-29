import json


# Function to load product data and discounts from the file
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
        json.dump(discounts, file, indent=4)  # Write the dictionary as JSON with indentation


# Load the initial product data from the file
discounts = discount_management()


# Helper function to validate discount input
def validate_discount_input():
    while True:
        try:
            discount = float(input("Enter discount percentage (0-100): "))
            if 0 <= discount <= 100:  # Ensure discount is within valid range
                return discount
            else:
                print("⚠️ Invalid input. Discount must be between 0 and 100.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid number.")


# Function to add a discount (or update it if it exists)
def add_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        discount = validate_discount_input()  # Use the validated input
        discounts[product_code]['Discount'] = f"{discount}%"  # Update only the discount field
        save_discounts(discounts)  # Save the updated discounts to the file
        print(f"Discount for product {product_code} updated to {discount}%.")
    else:
        print(f"|⚠️Product {product_code} not found. Please add the product before applying a discount.|")


# Function to delete a discount (set to 0%)
def delete_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        discounts[product_code]['Discount'] = "0%"  # Reset discount to 0%
        save_discounts(discounts)  # Save the updated discounts to the file
        print(f"Discount for product {product_code} has been reset to 0%.")
    else:
        print(f"|⚠️No discount found for product {product_code}.|")


# Function to modify an existing discount
def modify_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        new_discount = validate_discount_input()  # Use the validated input
        discounts[product_code]['Discount'] = f"{new_discount}%"  # Update the discount field
        save_discounts(discounts)  # Save the updated discounts to the file
        print(f"Discount for product {product_code} updated to {new_discount}%.")
    else:
        print(f"|⚠️No discount found for product {product_code}. Use 'add' to create a new discount.|")


# Display all products with discounts
def display_discounts():
    if discounts:
        print("Current Discounts and Product Details:")
        for product_code, product_info in discounts.items():
            print(f"Product Code: {product_code}")
            for key, value in product_info.items():
                print(f"  {key}: {value}")
    else:
        print("|⚠️No discounts available!|")


# Let user choose an option
def manage_discounts():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'DISCOUNT MANAGEMENT')
        print('-----------------------------------------------')
        print("1. Add/Update Discount")
        print("2. Reset Discount")
        print("3. View All Discounts")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_discount()
        elif choice == '2':
            delete_discount()
        elif choice == '3':
            display_discounts()
        elif choice == '4':
            confirm_exit = input("Are you sure you want to exit? yes=y / no=n: ").lower()
            if confirm_exit == 'y':
                print("***Exiting Discount Management. Goodbye!***")
                break
            else:
                print("Returning to the menu.")
        else:
            print("|⚠️Invalid option. Please try again.|")


# Call the function
manage_discounts()
