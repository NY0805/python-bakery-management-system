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

# Save the updated reviews to a file
def save_reviews(reviews):
    with open("customer_reviews.txt", "w") as file:
        json.dump(reviews, file, indent=4)

# Allow the customer to submit a review for a purchased product
def submit_review():
    # Get username and review details
    username = input("Enter your username: ")
    product_name = input("Enter the product name: ")
    review_text = input("Enter your review: ")
    rating = input("Rate your product (1-5): ")

    # Validate rating input
    if not rating.isdigit() or int(rating) not in range(1, 6):
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    # Create a review entry
    review = {
        "username": username,
        "product_name": product_name,
        "review_text": review_text,
        "rating": int(rating)
    }

    # Load existing reviews
    reviews = load_reviews()

    # Add new review to the list
    reviews.append(review)

    # Save updated reviews
    save_reviews(reviews)

    print("Thank you for submitting your feedback! We have received your review.")

submit_review()