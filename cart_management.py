import json

def load_data_from_cart():
    try:
        with open('customer_order_list.txt', 'r') as file:
            content = file.read().strip()
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {}
            else:
                return {}
    except FileNotFoundError:
        return {}


def load_inventory():
    try:
        with open('inventory_product.txt', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_cart_to_file(cart):
    with open('customer_order_list.txt', 'w') as file:
        json.dump(cart, file, indent=4)


def get_product_price(product_id, inventory):
    for item in inventory:
        if item['product_id'] == product_id:
            return item['price']
    return None


def add_item_to_cart():
    cart = load_data_from_cart()
    inventory = load_inventory()
    username = input("Enter your username: ")

    # Check if user's cart exists
    if username in cart:
        user_cart = cart[username]
    else:
        cart[username] = []
        user_cart = cart[username]

    product_id = input("Enter the product ID to add to cart: ")
    quantity = int(input("Enter the quantity: "))

    # Check if product exists in inventory
    product_price = get_product_price(product_id, inventory)
    if not product_price:
        print("Product not found in inventory.")
        return

    # Check if product already exists in user's cart
    for item in user_cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

    # If product not in cart, add new item
    user_cart.append({"product_id": product_id, "quantity": quantity})
    save_cart_to_file(cart)
    print("Item added to cart.")


def remove_item_from_cart():
    cart = load_data_from_cart()
    username = input("Enter your username: ")

    if username not in cart:
        print("No cart found for this username.")
        return

    user_cart = cart[username]
    product_id = input("Enter the product ID to remove from cart: ")

    # Filter out the item to remove
    new_cart = [item for item in user_cart if item['product_id'] != product_id]

    if len(new_cart) == len(user_cart):
        print("Item not found in cart.")
    else:
        cart[username] = new_cart
        save_cart_to_file(cart)
        print("Item removed from cart.")


def modify_item_in_cart():
    cart = load_data_from_cart()
    username = input("Enter your username: ")

    if username not in cart:
        print("No cart found for this username.")
        return

    user_cart = cart[username]
    product_id = input("Enter the product ID to modify: ")

    for item in user_cart:
        if item['product_id'] == product_id:
            new_quantity = int(input("Enter the new quantity: "))
            item['quantity'] = new_quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

    print("Item not found in cart.")


def view_cart():
    cart = load_data_from_cart()
    username = input("Enter your username: ")

    if username not in cart:
        print("No cart found for this username.")
        return

    user_cart = cart[username]
    if not user_cart:
        print("Your cart is empty.")
        return

    inventory = load_inventory()
    total_price = 0

    print("Your Cart:")
    for item in user_cart:
        product_id = item['product_id']
        quantity = item['quantity']
        product_price = get_product_price(product_id, inventory)
        if product_price is not None:
            item_total = product_price * quantity
            total_price += item_total
            print(
                f"Product ID: {product_id}, Quantity: {quantity}, Price per unit: ${product_price:.2f}, Total: ${item_total:.2f}")
        else:
            print(f"Product ID: {product_id} not found in inventory.")

    print(f"Total Price: ${total_price:.2f}")
