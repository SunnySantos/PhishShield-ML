import requests
from requests.exceptions import RequestException
import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time

def is_url_online(url, retries=3):
    """Checks if the URL is online by trying both http and https with a retry backoff."""
    for attempt in range(retries):
        for scheme in ['http://', 'https://', 'http://www.', 'https://www.']:
            full_url = f"{scheme}{url}" if not urlparse(url).scheme else url
            try:
                response = requests.head(full_url, timeout=5)
                if response.status_code == 200:
                    return full_url
            except RequestException:
                time.sleep(2 ** attempt)  # Exponential backoff
    return None

def check_url_and_process(id, url):
    """Check the URL and decide whether to update or delete."""
    if '://' not in url:  # If the URL does not have a scheme
        updated_url = is_url_online(url)
        if updated_url:
            return ('update', id, updated_url)
        else:
            return ('delete', id, None)
    else:
        # If URL already has a scheme, check if it's online
        if is_url_online(url):
            return ('keep', id, url)
        else:
            return ('delete', id, None)

def process_batch(urls, connection):
    """Process a single batch of URLs."""
    update_queries = []
    delete_ids = set()
    cursor = connection.cursor()

    # Use ThreadPoolExecutor for parallel URL checking with limited workers
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(check_url_and_process, id, url): (id, url) for id, url in urls}
        for future in as_completed(futures):
            try:
                action, id, updated_url = future.result()
                if action == 'update':
                    cursor.execute("SELECT id FROM allowlist WHERE url = %s", (updated_url,))
                    duplicate = cursor.fetchone()
                    if duplicate and duplicate[0] != id:
                        delete_ids.add(id)
                    else:
                        update_queries.append((updated_url, id))
                elif action == 'delete':
                    delete_ids.add(id)
            except Exception as e:
                print(f"Error processing URL {futures[future]}: {e}")

    # Perform batch update
    if update_queries:
        cursor.executemany("UPDATE allowlist SET url = %s WHERE id = %s", update_queries)
        connection.commit()

    # Perform batch delete
    if delete_ids:
        cursor.execute(f"DELETE FROM allowlist WHERE id IN ({', '.join(map(str, delete_ids))})")
        connection.commit()

    cursor.close()

def batch_process():
    # Connect to MySQL database
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'phishshield'
    }
    connection = mysql.connector.connect(**db_config)
    
    # Fetch total count and process in batches of 100
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM allowlist")
    total_urls = cursor.fetchone()[0]
    batch_size = 100
    offset = 0

    print(f"Total URLs to process: {total_urls}")

    while offset < total_urls:
        cursor.execute("SELECT id, url FROM allowlist LIMIT %s OFFSET %s", (batch_size, offset))
        urls = cursor.fetchall()

        if not urls:
            break  # Exit if no more rows to process

        print(f"Processing batch with offset {offset}")

        # Process the current batch
        process_batch(urls, connection)
        
        offset += batch_size

    cursor.close()
    connection.close()

if __name__ == "__main__":
    batch_process()