import requests
import json
from datetime import datetime, date


# Function to fetch available pets from the server
def show_available_pets():
    # Sends a GET request to the server to retrieve available pets
    result = requests.get('http://127.0.0.1:5000/availability', headers={'content-type': 'application/json'})
    return result.json()


# Function to fetch adoption information from the server
def show_adoption_info():
    # Sends a GET request to the server to retrieve adoption information
    result = requests.get('http://127.0.0.1:5000/adoption-info', headers={'content-type': 'application/json'})
    return result.json()


# Function to adopt a new pet by sending adoption details to the server
def adopt_a_new_pet(pet_id, name, contact_info, adoption_date):
    # Converts the adoption_date to a string in ISO format
    adoption_date_str = adoption_date.isoformat()

    # Adoption details that are to be sent to the server
    adoption = {
        "pet_id": pet_id,
        "adopter_name": name,
        "contact_info": contact_info,
        "adoption_date": adoption_date_str,
    }

    # Sends a PUT request to the server with the adoption details
    result = requests.put(
        'http://127.0.0.1:5000/adopt',
        headers={'content-type': 'application/json'},
        data=json.dumps(adoption)
    )
    return result.json()


# Function to cancel an adoption by sending the adoption ID to the server
def cancel_an_adoption(adoption_id):
    # Sends a DELETE request to the server to cancel the adoption
    requests.delete(f'http://127.0.0.1:5000/cancel/{adoption_id}',
                    headers={'content-type': 'application/json'})


# Function to display available pets in a formatted table
def display_availability(data):
    # Prints the column headers for the table
    print("{:<15} | {:<15} | {:<15} | {:<15} | {:<30} | {:<15}".format(
        'PET ID', 'NAME', 'SPECIES', 'AGE', 'DESCRIPTION', 'AVAILABILITY'))
    print('-' * 130)  # Added dashes for visual separation

    # Iterates over each pet in the data and prints its details
    for item in data:
        print("{:<15} | {:<15} | {:<15} | {:<15} | {:<30} | {:<15}".format(
            item['pet_id'], item['name'], item['species'], item['age'], item['description'], item['available']
        ))


# Function to display adoption information in a formatted table
def display_adoption_info(data):
    # Prints the column headers for the table
    print("{:<15} | {:<15} | {:<15} | {:<22} | {:<15}".format(
        'ADOPTION ID', 'PET ID', 'ADOPTER NAME', 'CONTACT INFO', 'ADOPTION DATE'))
    print('-' * 110)  # Added dashes for visual separation

    # Iterates over each adoption in the data and prints its details
    for item in data:
        # Converts the adoption_date string to a datetime object
        adoption_date = datetime.strptime(item['adoption_date'], '%a, %d %b %Y %H:%M:%S %Z')
        # Formats the adoption date to remove the time component
        adoption_date_formatted = adoption_date.strftime('%a, %d %b %Y')
        print("{:<15} | {:<15} | {:<15} | {:<22} | {:<15}".format(
            item['adoption_id'], item['pet_id'], item['adopter_name'], item['contact_info'], adoption_date_formatted
        ))


# Main function to run the application
def run():
    print()
    print('Hello, welcome to Kharina\'s pet shop!')
    print()

    choice = input('Would you like to adopt a pet or cancel an adoption? Type "adopt" or "cancel". ')
    print()

    if choice == 'adopt':
        # Fetches and displays available pets
        availability_columns = show_available_pets()
        display_availability(availability_columns)
        print()

        pet_id = input('What pet would you like to adopt? Please input the pet ID! ')
        print()

        # Validates the pet ID
        valid_pet_ids = [pet['pet_id'] for pet in availability_columns]
        if pet_id == '' or int(pet_id) not in valid_pet_ids:
            print("Invalid pet ID. Please select a valid pet ID.")
            return

        print('Great choice!')

        adopter_name = input('Please enter your first and last name. ')
        contact_info = input('Please enter your email. ')
        # Sets the adoption date to today
        adoption_date = date.today()

        adopt_a_new_pet(pet_id, adopter_name, contact_info, adoption_date)
        print('Congrats! You have successfully adopted a pet! ')
        print()

        # Fetches and displays updated adoption information
        adoption_info_columns = show_adoption_info()
        display_adoption_info(adoption_info_columns)

        print()

        # Fetches and displays updated pet availability
        updated_availability_columns = show_available_pets()
        display_availability(updated_availability_columns)

    elif choice == 'cancel':
        # Fetches and displays adoption information
        adoption_info_columns = show_adoption_info()
        display_adoption_info(adoption_info_columns)

        print()

        adoption_id = input('Please enter your adoption ID for the adoption you\'d like to cancel. ')

        print()
        # Validates the adoption ID
        valid_adoption_ids = [adoption['adoption_id'] for adoption in adoption_info_columns]
        if adoption_id == '' or int(adoption_id) not in valid_adoption_ids:
            print("Invalid adoption ID. Please select a valid adoption ID.")
            return

        cancel_an_adoption(adoption_id)

        # Fetches and displays updated adoption information
        updated_adoption_info_columns = show_adoption_info()
        display_adoption_info(updated_adoption_info_columns)
        print('Your adoption has been successfully cancelled!')

    else:
        print('That isn\'t a valid option, please try again!')
        return

    print()
    print('Please come again!')


# Runs the application
if __name__ == '__main__':
    run()
