import json


def load_review():
    try:
        with open('customer_reviews.txt', 'r') as file:
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


def submit_review(username):
    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'PRODUCT REVIEW')
    print('-----------------------------------------------')

    # Load customer order list to check if the user has purchased anything
    order_list = load_order_list()
    if username not in order_list:
        print('|⚠️ You have not purchased any items. Please buy something before writing a review!|')
        return

    # Check if the user has any items with a status other than 'Canceled'
    has_purchased = any(item['status'] != 'Canceled' for item in order_list[username]['items ordered'])
    if not has_purchased:
        print('|⚠️ You have not purchased any items. Please buy something before writing a review!|')
        return

    # Allow customer to enter review details
    review_text = input('Enter your review: ')
    rating = input('Rate your product (1-5): ')

    # Validate the rating to ensure it's between 1 and 5
    while not validation_rating(rating):
        print('|⚠️ Invalid rating. Please enter a number between 1 and 5!|')
        rating = input('Rate your product (1-5): ')

    # Load existing reviews
    reviews = load_review()
    # Get the first product name from the order list for the user
    product_name = order_list[username]['items ordered'][0]['product_name']  # Get the first product for simplicity

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

# Assuming you have access to the logged-in username
username = "the_logged_in_username"  # Replace this with the actual logged-in username

# Call submit_review with the username
#submit_review(username)
