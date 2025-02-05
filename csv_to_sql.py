import csv
import re

# File paths
csv_file = 'phishtank_dataset.csv'
sql_file = 'insert_queries.sql'

# SQL script generator function with escaping and duplicate handling
def generate_blocklist_sql_from_csv(csv_file, sql_file):
    benign_urls = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Gather all benign URLs in a list
        for row in reader:
            if row['type'].strip().lower() != 'benign':
                url = re.escape(row['url'])  # Escape special characters in the URL
                url = url.replace("'", "''")  # Escape single quotes for SQL
                
                benign_urls.append(url)
    
    with open(sql_file, 'w', encoding='utf-8') as sql:
        print("Starting batch insert into reports...")
        # Batch insert into reports with IGNORE to avoid duplicates
        sql.write("INSERT IGNORE INTO reports (url, username) VALUES\n")
        sql.write(",\n".join([f"('{url}', 'John Smith')" for url in benign_urls]) + ";\n\n")
        print("Completed batch insert into reports.")

        print("Starting batch insert into blocklist...")
        # Batch insert into blocklist with IGNORE to avoid duplicates
        sql.write("INSERT IGNORE INTO blocklist (url, approved_by) VALUES\n")
        sql.write(",\n".join([f"('{url}', 1)" for url in benign_urls]) + ";\n\n")
        print("Completed batch insert into blocklist.") 

        print("Writing update statement...")
        # Update reports with blocklist_website_id using JOIN syntax
        sql.write("""
            UPDATE reports
            JOIN blocklist ON reports.url = blocklist.url
            SET reports.blocklist_website_id = blocklist.id;
        """)
        print("Update statement written.")

    print(f"SQL file '{sql_file}' generated successfully.")

    # SQL script generator function with escaping and duplicate handling
def generate_allowlist_sql_from_csv(csv_file, sql_file):
    benign_urls = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Gather all benign URLs in a list
        for row in reader:
            if row['type'].strip().lower() == 'benign':
                url = re.escape(row['url'])  # Escape special characters in the URL
                url = url.replace("'", "''")  # Escape single quotes for SQL
                
                benign_urls.append(url)
    
    with open(sql_file, 'w', encoding='utf-8') as sql:
        print("Starting batch insert into reports...")
        # Batch insert into reports with IGNORE to avoid duplicates
        sql.write("INSERT IGNORE INTO reports (url, username) VALUES\n")
        sql.write(",\n".join([f"('{url}', 'John Smith')" for url in benign_urls]) + ";\n\n")
        print("Completed batch insert into reports.")

        print("Starting batch insert into allowlist...")
        # Batch insert into allowlist with IGNORE to avoid duplicates
        sql.write("INSERT IGNORE INTO allowlist (url, approved_by) VALUES\n")
        sql.write(",\n".join([f"('{url}', 1)" for url in benign_urls]) + ";\n\n")
        print("Completed batch insert into allowlist.") 

        print("Writing update statement...")
        # Update reports with allowlist_website_id using JOIN syntax
        sql.write("""
            UPDATE reports
            JOIN allowlist ON reports.url = allowlist.url
            SET reports.allowlist_website_id = allowlist.id;
        """)
        print("Update statement written.")

    print(f"SQL file '{sql_file}' generated successfully.")

# Run the function
# generate_allowlist_sql_from_csv(csv_file, sql_file)
generate_blocklist_sql_from_csv(csv_file, sql_file)

#source C:/Users/Renz/Documents/machine-learning/insert_queries.sql