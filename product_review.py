import json


def load_reviews():
    try:
        # Open the file and read the content
        with open('customer_reviews.txt', 'r') as file:
            content = file.read().strip()

        if content:  # Check if the file is not empty
            try:
                return json.loads(content)  # Parse the content as JSON
            except json.JSONDecodeError:
                print("Error loading review data. The file format might be incorrect.")
                return []  # Return an empty list if parsing fails
        else:
            return []  # Return an empty list if the file is empty

    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist


# Save customer's review to txt file
def save_reviews(new_review):
    try:
        # Try to read the existing reviews
        with open('customer_reviews.txt', 'r') as file:
            reviews = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        reviews = []

    # Append the new review to the existing reviews
    reviews.append(new_review)

    # Write all reviews back to the file
    with open('customer_reviews.txt', 'w') as file:
        json.dump(reviews, file, indent=4)


# Validate that the rating is a number between 1 and 5
def validation_rating(rating):
    try:
        if rating.isdigit() and int(rating) in range(1, 6):
            return True
        else:
            return False
    except ValueError:
        return False


# Allow the customer to submit a review for a purchased product
def submit_review():
    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'PRODUCT REVIEW')
    print('-----------------------------------------------')

    # Get username and review details
    username = input('Enter your username: ')
    product_name = input('Enter the product name: ')
    review_text = input('Enter your review: ')
    rating = input('Rate your product (1-5): ')

    # Validate rating input
    while not validation_rating(rating):
        print('|⚠️Invalid rating. Please enter a number between 1 and 5!|')

    # Create the new review dictionary
    review = {
        'username': username,
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating)
    }

    # Save the new review
    save_reviews(review)

    print('*****Thank you for your feedback!*****')
    print('Your review has been successfully received.')
