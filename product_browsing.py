import json
import product_menu

product_data = product_menu.product_data


# Load product categories and names from baker_product_keeping.txt
def load_categories():
    try:
        with open('baker_product_keeping.txt', 'r') as file:
            categories = json.load(file)  # Assuming this is structured as a JSON object
            return {v["category"]: v["product_name"] for k, v in categories.items()}  # Map categories to product names
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

    # Menu options for the customer
    while True:
        print("Please choose an option:")
        print("1. Search for products by category")
        print("2. Exit")

        choice = input("Enter your choice (1/2): ")

        if choice == '1':
            category_input = input("Please enter the product category you want to search for: ")

            # Check if the category exists in the baker's product list
            if category_input in categories:
                print(f"Products in category '{category_input}':")
                print('===============================================')

                # Loop through the products to find matches based on the category and product name
                for product_code, product in products.items():
                    if product["product_name"].lower() == categories[category_input].lower():  # Match product name
                        print(f'Product Code: {product_code}')
                        print(f'Product Name: {product["product_name"]}')
                        print(f'Price: {product["price"]}')
                        print(f'Description: {product["description"]}')
                        print('-----------------------------------------------')
            else:
                print(f"The category '{category_input}' does not exist.")

        elif choice == '2':
            print("Thank you for visiting our system. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

browse_products()


