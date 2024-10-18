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


def add_discount():
    # Attempt to read existing product data
    try:
        with open('product_discount.txt', 'r') as file:  # Open the file and read
            content = file.read().strip()  # Strip unnecessary whitespaces
            if content:  # Check if the file is not empty
                try:
                    products = json.loads(content)  # Parse the content as JSON
                except json.JSONDecodeError:
                    products = {}  # Return empty dictionary if parsing fails
            else:
                products = {}  # Return empty dictionary if the file is empty
    except FileNotFoundError:
        products = {}  # Return empty dictionary if the file does not exist

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
        if stock_input.isdigit():  # Check if the input is a digit
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
            print("Invalid input. Please enter a numeric value for price.")

    # Validate discount input
    while True:
        discount_input = input("Enter discount percentage: ")
        try:
            discount = float(discount_input)
            if discount >= 0:  # Ensure discount is non-negative
                break  # Break the loop if valid input
            else:
                print("Please enter a valid positive number for discount.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for discount.")

    try:
        with open("product_discount.txt", "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        products = {}  # If the file doesn't exist, start with an empty dictionary

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

    # Write back to the file, retaining existing products
    with open("product_discount.txt", "w") as f:
        json.dump(products, f, indent=4)

    print(f"New product {product_name} added with a discount of {discount}%.")


# Function to delete a discount (set to 0% or remove product)
def delete_discount():
    product_code = input("Enter product code: ")
    if product_code in discounts:
        del discounts[product_code]  # Remove the product from the discounts
        save_discounts(discounts)  # Save the updated discounts to the file
        print(f"Product {product_code} and its discount have been deleted.")
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
        print(f"|⚠️No discount found for product {product_code}. Use 'Add Discount' to create a new discount.|")


# Display all products with discounts
# Display all products with discounts
def display_discounts():
    if discounts:
        print('\n' + '•' * 60 + ' Current Discounts and Product Details ' + '•' * 60 + '\n')

        # Print header with proper column widths for alignment
        print(f"{'Product Code'.ljust(15)}{'Product Name'.ljust(25)}{'Price'.ljust(15)}{'Discount'.ljust(15)}{'Stock'.ljust(10)}")
        print('-' * 80)

        has_discount = False  # Track if any products with discounts exist

        for product_code, product_info in discounts.items():
            # Extract product details
            product_name = product_info.get('Product Name', '').ljust(25)
            price = product_info.get('Price', '').ljust(15)
            discount = product_info.get('Discount', '')
            stock = str(product_info.get('Stock', '')).ljust(10)

            # Only display products with a discount greater than 0%
            discount_value = float(discount[:-1]) if discount else 0  # Extract the numeric value from the string
            if discount_value > 0:  # Check if the discount is greater than 0%
                print(f"{product_code.ljust(15)}{product_name}{price}{discount.ljust(15)}{stock}")
                has_discount = True  # Set flag to True if we display at least one discount

        print('-' * 80 + '\n')

        if not has_discount:  # If no products with discounts were displayed
            print("|⚠️ No products with discounts available! |")
    else:
        print("|⚠️ No discounts available! |")


# Main menu for managing discounts
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


# Start the discount management system
manage_discounts()
