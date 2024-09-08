def load_reviews(): #Load existing reviews from a file (reviews.json).
    try:
        with open("reviews.txt", "r") as file:
            reviews = json.load(file)
        return reviews
    except FileNotFoundError:
        # If file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        print("Error loading review data. The file format might be incorrect.")
        return []


def save_reviews(reviews): #Save the updated reviews to a file
    with open("reviews.txt", "w") as file:
        json.dump(reviews, file, indent=4)


def submit_review():# Allow the customer to submit a review for a purchased product
    # Get user input
    product_name = input("Enter the name of the product you want to review: ")
    review_text = input("Enter your review: ")
    rating = input("Rate your product (1-5): ")

    # Validate rating input
    if not rating.isdigit() or int(rating) not in range(1, 6):
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    # Create a review entry
    review = {
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

