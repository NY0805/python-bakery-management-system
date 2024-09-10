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

    if username not in cart:
        cart[username] = []

    user_cart = cart[username]
    product_id = input("Enter the product ID to add to cart: ")
    quantity = int(input("Enter the quantity: "))

    product_price = get_product_price(product_id, inventory)
    if not product_price:
        print("Product not found in inventory.")
        return

    for item in user_cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

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


def create_new_cart():
    """Create a new cart ID and add it to the dictionary."""
    cart = load_data_from_cart()
    new_cart_id = "cart" + str(len(cart) + 1)
    cart[new_cart_id] = []  # Add a new, empty cart for the user
    save_cart_to_file(cart)
    print(f"New cart created with ID: {new_cart_id}")
    return new_cart_id


def make_payment(cart_id):
    """Process payment based on the cart ID."""
    cart = load_data_from_cart()

    if cart_id not in cart:
        print("Cart cannot be found.")
        return

    cart_items = cart[cart_id]
    inventory = load_inventory()
    total_price = 0

    for item in cart_items:
        product_id = item['product_id']
        quantity = item['quantity']
        product_price = get_product_price(product_id, inventory)
        if product_price is not None:
            total_price += product_price * quantity

    print(f"Total price for cart {cart_id}: ${total_price:.2f}")

    confirmation = input("Do you want to confirm the payment? (yes/no): ").lower()

    if confirmation == 'yes':
        order_id = len(cart) + 1
        order = {
            "order_id": order_id,
            "username": cart_id,  # Use cart ID as username for simplicity
            "items_ordered": [f"Product ID: {item['product_id']} x{item['quantity']}" for item in cart_items],
            "total_price": total_price,
            "status": "Paid"
        }
        with open('customer_order_list.txt', 'r') as file:
            all_orders = json.load(file)
        all_orders[str(order_id)] = order
        with open('customer_order_list.txt', 'w') as file:
            json.dump(all_orders, file, indent=4)
        print("Payment successful! Thank you for your purchase.")
        cart[cart_id] = []  # Clear the cart after payment
        save_cart_to_file(cart)
    else:
        order_id = len(cart) + 1
        order = {
            "order_id": order_id,
            "username": cart_id,  # Use cart ID as username for simplicity
            "items_ordered": [f"Product ID: {item['product_id']} x{item['quantity']}" for item in cart_items],
            "total_price": total_price,
            "status": "Cancelled"
        }
        with open('customer_order_list.txt', 'r') as file:
            all_orders = json.load(file)
        all_orders[str(order_id)] = order
        with open('customer_order_list.txt', 'w') as file:
            json.dump(all_orders, file, indent=4)
        print("Your payment has been cancelled.")


# Example usage
new_cart_id = create_new_cart()  # Create a new cart for a new customer

# Let the user make a payment using their new cart ID
cart_id_input = input("Please enter your cart ID to make a payment: ")
make_payment(cart_id_input)

