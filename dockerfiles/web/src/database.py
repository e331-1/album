import os
import time
import mysql.connector
while True:
    try:
        conn = mysql.connector.connect(
            host='db',
            port='3306',
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database="album"
        )
        break
    except mysql.connector.errors.DatabaseError as e:
        print(f"Error connecting to database: {e}")
        print(os.environ.get('MYSQL_USER'))
        time.sleep(5)
