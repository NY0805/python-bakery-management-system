import  json
from customer_product_review import load_review

# Define the function that saves information to the file
def save_info(review):
    file = open('manager_customer_feedback.txt', 'w')  # open the file to write
    json.dump(review, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


review = load_review()


def monitor_review():
    while True:
        print('\n', '\t'*13, 'CUSTOMER FEEDBACK')
        print('-' * 125)
        header = []  # create a list for headers
        for value in review.values():  # access the values of order_list
            for sub_key, sub_value in value.items():  # access the subkey and sub value in the value of order_list
                header.append(sub_key.title().replace('_', ' '))  # append other details of orders into the header list and replace all underscore with space to enhance readability
            break

        print(f'{header[0]:<19}{header[1]:<19}{header[2]:<20}{header[3]:<24}{header[4]:<26}{header[5]}')  # display the headers
        print('-' * 125)
