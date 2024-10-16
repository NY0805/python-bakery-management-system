import json


def load_review():
    try:
        with open('customer_reviews.txt', 'r') as file:
            content = file.read().strip()
        if content:
            return json.loads(content)
        else:
            return {}
    except FileNotFoundError:
        return {}


def save_reviews(new_review):
    with open('customer_reviews.txt', 'w') as file:
        json.dump(new_review, file, indent=4)


def load_order_list():
    try:
        with open('customer_order_list.txt', 'r') as file:
            content = file.read().strip()
        if content:
            return json.loads(content)
        else:
            return {}
    except FileNotFoundError:
        return {}


def validation_rating(rating):
    return rating.isdigit() and int(rating) in range(1, 6)


def submit_review(logged_in_username):
    print('\n-----------------------------------------------')
    print('\t\t\tPRODUCT REVIEW')
    print('-----------------------------------------------')

    # Initialize variables to check for valid purchase and product name
    valid_purchase_found = False
    product_name = None

    # Load order list to check if the user has completed any purchases
    order_list = load_order_list()  # Ensure the order list is loaded here

    # Check if the user has completed any purchases
    for order_id, order_data in order_list.items():  # Use .items() method to iterate through the dictionary
        if order_data["username"] == logged_in_username:  # Match with logged-in username
            if order_data["status"] == "Payment Completed":
                valid_purchase_found = True
                product_name = order_data['items_ordered'][0]  # Get the first product name
                review_text = input('Enter your review: ')
                rating = input('Rate your product (1-5): ')
                break  # Exit the loop after finding a valid order

    # Check if no valid purchase was found
    if not valid_purchase_found:  # Use if instead of else if
        print('|⚠️ You have not completed any purchases. Please buy something before writing a review!|')
        return

    # Load existing reviews
    reviews = load_review()

    # Update the review for the user
    reviews[logged_in_username] = {
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating)  # Convert rating to an integer
    }

    # Save the updated reviews
    save_reviews(reviews)
    print()
    print('***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')

    reviews = load_review()

    # Update the review for the user
    reviews[username] = {
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating)
    }

    # Save the updated reviews
    save_reviews(reviews)
    print()
    print('***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')


#submit_review