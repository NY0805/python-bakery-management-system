import json


# Load product categories and names from baker_product_keeping.txt
def load_categories():
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


# Load product details from manager_product_inventory.txt
def load_product_details():
    try:
        file = open('manager_product_inventory.txt', 'r')  # open the file and read
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


# Function to enable customer browse product
def browse_products():
    # Load data
    categories = load_categories()
    products = load_product_details()

    print('\n-----------------------------------------------')
    print('\t\t\tPRODUCT BROWSING')
    print('-----------------------------------------------')

    # Check if categories are available and display them to the user
    if categories:
        print("\n✨ Welcome to our bakery! We have a variety of product categories for you to explore:")
        product_categories = set([item["category"] for item in categories.values()])
        for category in product_categories:
            print(f"- {category}")
        print("\nFeel free to browse the products by selecting a categoryor view the full menu!\n")
    else:
        print("No categories available at the moment.\n")

    # Provide customers with options
    while True:
        print()
        print("Please choose an option:")
        print("1. Search for products by category")
        print("2. View full menu")
        print("3. Exit")

        options = input("Enter your choice (1/2/3): ")

        if options == '1':
            category_input = input("Please enter the product category you want to search for: ")

            # Check if the category exists
            if any(item["category"].lower() == category_input.lower() for item in categories.values()):
                print()
                print(f"Products in category '{category_input}':")
                print('===============================================')

                # Loop through categories find matching products from the product details
                for product_code, product in products.items():
                    # Get the matching category from baker_product_keeping
                    if product_code in categories and categories[product_code]["category"].lower() == category_input.lower():
                        print(f'Product Code: {product_code}')
                        print(f'Product Name: {product["product_name"]}')
                        print(f'Price: {product["price"]}')
                        print(f'Description: {product["description"]}')
                        print('-----------------------------------------------')
            else:
                print(f"The category '{category_input}' does not exist.")
                print()

        elif options == '2':
            import product_menu  # Display the full menu from product_menu.py
            product_menu.menu()
        elif options == '3':
            print("Thank you for visiting our system. Goodbye!")
            break

        else:
            print("|⚠️Invalid choice, please try again.|")



