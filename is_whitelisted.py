import mysql.connector
from urllib.parse import urlparse

def is_whitelisted(url):
    parsed_url = urlparse(url)

    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your database username
        password="",  # Change to your database password
        database="phishshield"
    )
    cursor = connection.cursor()

    # Prepare and execute the query
    query = "SELECT COUNT(*) FROM allowlist WHERE url LIKE %s"
    cursor.execute(query, (f'%{parsed_url.netloc}%',))
    
    count = cursor.fetchone()[0]  # Get the count from the result

    cursor.close()
    connection.close()

    print('Is Whitelisted:', count > 0)
    
    return count > 0  # Return True if whitelisted, otherwise False

# Example usage
url_to_check = 'https://www.google.com'
is_whitelisted(url_to_check)