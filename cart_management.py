def load_cart_from_file():
    try:
        with open('cart.txt', 'r') as file:
            content = file.read().strip()
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return []
            else:
                return []
    except FileNotFoundError:
        return []

def save_cart_to_file(cart):
    with open('cart.txt', 'w') as file:
        json.dump(cart, file, indent=4)

def add_item_to_cart():
    cart = load_cart_from_file()
    product_id = input("Enter the product ID to add to cart: ")
    quantity = int(input("Enter the quantity: "))

    # Check if product already exists in cart
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

    # If product not in cart, add new item
    cart.append({"product_id": product_id, "quantity": quantity})
    save_cart_to_file(cart)
    print("Item added to cart.")

def remove_item_from_cart():
    cart = load_cart_from_file()
    product_id = input("Enter the product ID to remove from cart: ")

    # Filter out the item to remove
    new_cart = [item for item in cart if item['product_id'] != product_id]

    if len(new_cart) == len(cart):
        print("Item not found in cart.")
    else:
        save_cart_to_file(new_cart)
        print("Item removed from cart.")

def modify_item_in_cart():
    cart = load_cart_from_file()
    product_id = input("Enter the product ID to modify: ")

    for item in cart:
        if item['product_id'] == product_id:
            new_quantity = int(input("Enter the new quantity: "))
            item['quantity'] = new_quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

    print("Item not found in cart.")

def view_cart():
    cart = load_cart_from_file()
    if not cart:
        print("Your cart is empty.")
        return

    print("Your Cart:")
    for item in cart:
        print(f"Product ID: {item['product_id']}, Quantity: {item['quantity']}")

def load_orders(): #Load the order data from a file
    try:
        with open("orders.txt", "r") as file:
            orders = json.load(file)
        return orders
    except FileNotFoundError:
        print("Order data not found. Please make sure the file exists.")
        return []
    except json.JSONDecodeError:
        print("Error loading order data. The file format might be incorrect.")
        return []