import mysql.connector
from config import HOST, USER, PASSWORD

db_name = 'PetAdoption'


# Custom exception class for database connection errors
class DbConnectionError(Exception):
    pass


# Function to establish a connection to the database
def connect_to_db(database_name):
    # Establishes a connection to the MySQL database using the provided host, user, password, and database name
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=database_name
    )
    print('Connected to DB')

    return connection


# Helper function to map database query results for available pets to a more readable format
def _map_availability_values(availability):
    mapped = []
    for item in availability:
        mapped.append({
            'pet_id': item[0],
            'name': item[1],
            'species': item[2],
            'age': item[3],
            'description': item[4],
            'available': 'Not Available' if item[5] == 0 else 'Available',
        })
    return mapped


def _map_adoption_values(adoption):
    mapped = []
    for item in adoption:
        mapped.append({
            'adoption_id': item[0],
            'pet_id': item[1],
            'adopter_name': item[2],
            'contact_info': item[3],
            'adoption_date': item[4],
        })
    return mapped


# Function to view available pets from the database
def view_available_pets():
    try:
        # Connects to the database
        db_connection = connect_to_db(db_name)
        cursor = db_connection.cursor()
        print('Connected to DB')

        # SQL query to select all pets that are available
        query = '''
        SELECT * FROM Pets
        WHERE available = 1
        '''
        cursor.execute(query)

        # Fetches all results from the query
        result = cursor.fetchall()
        # Maps the results to a more readable format
        availability = _map_availability_values(result)
        cursor.close()

    except Exception:
        # Raises a custom exception if there's an error connecting to the database
        raise DbConnectionError("Failed to read data from DB")

    finally:
        # Ensures the database connection is closed
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return availability


# Function to view adoption information from the database
def view_adoption_info():
    try:
        db_connection = connect_to_db(db_name)
        cursor = db_connection.cursor()
        print('Connected to DB')

        # SQL query to select all adoption information
        query = '''
        SELECT * FROM Adoption
        '''

        cursor.execute(query)
        result = cursor.fetchall()
        adoption_info = _map_adoption_values(result)
        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return adoption_info


# Function to adopt a pet, updating both the Adoption and Pets tables
def adopt_a_pet(pet_id, adopter_name, contact_info, adoption_date):
    try:
        db_connection = connect_to_db(db_name)
        cursor = db_connection.cursor()
        print('Connected to DB')

        # SQL queries to insert adoption information and update pet availability
        first_query = f'''
        INSERT INTO Adoption (pet_id, adopter_name, contact_info, adoption_date)
        VALUES ({pet_id}, '{adopter_name}', '{contact_info}', '{adoption_date}')
        '''

        second_query = f'''
        UPDATE Pets
        SET available = 0
        WHERE pet_id = {pet_id}
        '''

        cursor.execute(first_query)
        cursor.execute(second_query)
        db_connection.commit()
        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# Function to cancel an adoption, updating both the Adoption and Pets tables
def cancel_adoption(adoption_id):
    try:
        db_connection = connect_to_db(db_name)
        cursor = db_connection.cursor()
        print('Connected to DB')

        # SQL queries to delete adoption information and update pet availability
        first_query = f'''
        DELETE FROM Adoption
        WHERE adoption_id = {adoption_id}
        '''

        second_query = f'''
        UPDATE Pets
        SET available = 1
        WHERE pet_id = (SELECT pet_id FROM Adoption WHERE adoption_id = {adoption_id})
        '''

        cursor.execute(first_query)
        cursor.execute(second_query)
        db_connection.commit()
        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
