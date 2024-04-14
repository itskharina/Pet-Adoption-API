from flask import Flask, jsonify, request
from db_utils import view_available_pets, adopt_a_pet, cancel_adoption, view_adoption_info, DbConnectionError

app = Flask(__name__)


# Route for the root URL, displays a welcome message
@app.route('/')
def welcome():
    return "Welcome to Kharina's Pet Shop, where you can adopt an animal of your choice!"


# Route to get adoption information
@app.route('/adoption-info')
def get_adoption_info():
    # Calls a function to retrieve adoption information from the database
    result = view_adoption_info()
    return jsonify(result)


# Route to get information about available pets
@app.route('/availability')
def get_availability():
    # Calls a function to retrieve available pets from the database
    result = view_available_pets()
    return jsonify(result)


# Route to adopt a pet, accepts PUT requests
@app.route('/adopt', methods=['PUT'])
def book_adoption():
    result = request.get_json()
    # Calls a function to adopt a pet with the provided details
    adopt_a_pet(
        pet_id=result['pet_id'],
        adopter_name=result['adopter_name'],
        contact_info=result['contact_info'],
        adoption_date=result['adoption_date']
    )

    return result


# Route to cancel an adoption, accepts DELETE requests
@app.route('/cancel/<int:adoption_id>', methods=['DELETE'])
def delete_adoption(adoption_id):
    # Calls a function to cancel an adoption with the provided ID
    cancel_adoption(adoption_id)


if __name__ == '__main__':
    app.run(debug=True)
