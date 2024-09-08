def browse_products():
    try:
        # Load the products from the JSON file
        with open("products.txt", "r") as file:
            products = json.load(file)

        # Display the products to the customer
        print("\nAvailable Products:")
        for product in products:
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']}")
            print(f"Description: {product['description']}\n")

    except FileNotFoundError:
        print("Product data cannot be found.")