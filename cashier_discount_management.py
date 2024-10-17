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
        print(f"Product {product_code} already has a discount. Use 'Modify Discount' if you want to update it.")
    else:
        discount = validate_discount_input()  # Use the validated input
        product_name = input("Enter product name: ")
        price = input("Enter product price: ")
        stock = input("Enter product stock: ")
        # Add the new product with the discount
        discounts[product_code] = {
            'Product Name': product_name,
            'Price': f"{price}",
            'Discount': f"{discount}%",
            'Stock': stock
        }
        save_discounts(discounts)  # Save the updated discounts to the file
        print(f"Discount for product {product_code} added with {discount}%.")


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
