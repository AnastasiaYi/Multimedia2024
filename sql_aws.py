import mysql.connector
from mysql.connector import Error
import numpy as np


print("MySQL Connector/Python is installed successfully!")

def insert_image_data(values):
    try:
        connection = mysql.connector.connect(host='database-1.c5miekkcia0c.ap-southeast-2.rds.amazonaws.com',
                                            database='bird_db',
                                            user='admin',
                                            password='12345678')
        
        # create a new cursor object associated with connection, for using it to execute SQL queries or commands latter
        cursor = connection.cursor()  
        print("connected to database!")

        insert_query = """
        INSERT INTO image_data (image_class, feature_vector, img_path, hash_value)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, values)
        print("INSERTED")
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# from retreiveData.py  --->        
def fetch_image_data(image_id):
    """Fetches all attributes of a specific row based on the image_id."""
    # Database connection parameters
    config = {
        'host': 'database-1.c5miekkcia0c.ap-southeast-2.rds.amazonaws.com',
        'user': 'admin',
        'password': '12345678',
        'database': 'bird_db'
    }

    try:
        # Establishing the connection
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            # Create a cursor object
            cursor = connection.cursor()
            # SQL query to fetch data
            query = "SELECT image_class, feature_vector, img_path, hash_value FROM image_data WHERE image_id = %s"
            # Executing the query
            cursor.execute(query, (image_id,))
            # Fetching one record
            row = cursor.fetchone()
            if row:
                return {
                    'image_class': row[0],
                    'feature_vector': row[1],
                    'img_path': row[2],
                    'hash_value': row[3]
                }
            else:
                return "No record found."
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
    finally:
        # Closing the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
# <--- from retreiveData.py  
            
# Example data
image_class = 'Doudou'
# feature_vector = np.zeros((1, 1, 4096))
feature_vector = b'\x00\x01...'  # Your binary feature vector data
img_path = '/path/to/image.jpg'
hash_value = 'abcdef123456'
values = (image_class, feature_vector, img_path, hash_value)
insert_image_data(values)

image_data = fetch_image_data(1)
print(image_data)
