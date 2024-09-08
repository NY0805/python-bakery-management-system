def order_tracking():
    # Prompt the user to enter their Order ID
    order_id = input("Enter your Order ID: ")

    # Load orders data
    orders = load_orders()

    # Check if the order_id exists in the loaded orders data
    order_exists = False  # Initialize a flag to track if the order is found

    # Iterate over each order to find the matching order ID
    for order in orders:
        if order["order_id"] == order_id:
            order_exists = True
            order_status = order["status"]
            order_details = order["items"]

            # Display order information
            print(f"Order ID: {order_id}")
            print(f"Status: {order_status}")
            print(f"Details: {order_details}")
            break

    # If the order ID was not found, show an error message
    if not order_exists:
        print("Order ID cannot be found. Please check and try again.")