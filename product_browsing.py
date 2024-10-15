import json


# Load product categories and names from baker_product_keeping.txt
def load_categories():
    try:
        with open('baker_product_keeping.txt', 'r') as file:
            categories = json.load(file)  # Assuming this is structured as a JSON object
            return categories  # Return full category data
    except FileNotFoundError:
        print("Categories file not found!")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from categories file.")
        return {}


# Load product details from manager_product_inventory.txt
def load_product_details():
    try:
        with open('manager_product_inventory.txt', 'r') as file:
            content = file.read().strip()
            return json.loads(content)
    except FileNotFoundError:
        print("Products file not found!")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from products file.")
        return {}


def browse_products():
    # Load data
    categories = load_categories()
    products = load_product_details()

    print('\n-----------------------------------------------')
    print('\t\t\tPRODUCT BROWSING')
    print('-----------------------------------------------')

    # Introduce categories to customers
    if categories:
        print("\n✨ Welcome to our bakery! We have a variety of product categories for you to explore:")
        available_categories = set([item["category"] for item in categories.values()])
        for category in available_categories:
            print(f"- {category}")
        print("\nFeel free to choose a category to browse the products or view the full menu!\n")
    else:
        print("No categories available at the moment.\n")

    # Menu options for the customer
    while True:
        print("Please choose an option:")
        print("1. Search for products by category")
        print("2. View full menu")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            category_input = input("Please enter the product category you want to search for: ")

            # Check if the category exists in the baker's product list
            if any(item["category"].lower() == category_input.lower() for item in categories.values()):
                print(f"Products in category '{category_input}':")
                print('===============================================')

                # Loop through categories and match products from the product details
                for product_code, product in products.items():
                    # Get the corresponding category from baker_product_keeping
                    if product_code in categories and categories[product_code]["category"].lower() == category_input.lower():
                        print(f'Product Code: {product_code}')
                        print(f'Product Name: {product["product_name"]}')
                        print(f'Price: {product["price"]}')
                        print(f'Description: {product["description"]}')
                        print('-----------------------------------------------')
            else:
                print(f"The category '{category_input}' does not exist.")

        elif choice == '2':
            import product_menu
            product_menu.menu()
        elif choice == '3':
            print("Thank you for visiting our system. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


#browse_products()

