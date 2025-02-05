def sanitize_url(url):
    url = url.strip()  # Remove leading and trailing whitespace
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Add scheme if missing
    return url

import mysql.connector
from urllib.parse import urlparse

def is_whitelisted(url):
    parsed_url = urlparse(url)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your database username
        password="",  # Change to your database password
        database="phishshield"
    )
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM allowlist WHERE url LIKE %s"
    cursor.execute(query, (f'%{parsed_url.netloc}%',))
    
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    print('Is Whitelisted:', count > 0)
    
    return count > 0


def is_blocklisted(url):
    parsed_url = urlparse(url)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your database username
        password="",  # Change to your database password
        database="phishshield"
    )
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM blocklist WHERE url LIKE %s"
    cursor.execute(query, (f'%{parsed_url.netloc}%',))
    
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    print('Is Blocklisted:', count > 0)
    
    return count > 0


def is_reported(url):
    parsed_url = urlparse(url)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your database username
        password="",  # Change to your database password
        database="phishshield"
    )
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM reports WHERE allowlist_website_id IS NULL AND blocklist_website_id IS NULL AND url LIKE %s"
    cursor.execute(query, (f'%{parsed_url.netloc}%',))
    
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    print('Is Reported:', count > 0)
    
    return count > 0 