import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="153.92.15.41",
    user="u373793174_root",  # Change to your database username
    password="Js^:c@D3r>^3",  # Change to your database password
    database="u373793174_phishshield"
)

cursor = db.cursor()

safe_urls = ['https://www.facebook.com', 'https://www.google.com', 'https://www.youtube.com']

# Fetch safe URLs from the allowlist table
cursor.execute("SELECT url FROM allowlist limit 10")
safe_urls.extend([row[0] for row in cursor.fetchall()])

# Fetch malicious URLs from the blocklist table
cursor.execute("SELECT url FROM blocklist limit 10")
malicious_urls = [row[0] for row in cursor.fetchall()]

# Close the database connection
cursor.close()
db.close()

print('Safe URLs:', safe_urls)
print('Malicious URLs:', malicious_urls)
