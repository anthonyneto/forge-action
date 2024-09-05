import mysql.connector
from mysql.connector import Error

def create_database_and_user(host, user, password, new_db_name, new_user, new_user_password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name}")
            cursor.execute(f"CREATE USER IF NOT EXISTS '{new_user}'@'%' IDENTIFIED BY '{new_user_password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {new_db_name}.* TO '{new_user}'@'%'")
            cursor.execute("FLUSH PRIVILEGES")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
