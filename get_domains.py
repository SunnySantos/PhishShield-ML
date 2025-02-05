import pandas as pd
from urllib.parse import urlparse


def add_http():
    # Load the CSV file
    input_csv = 'malicious_phish2.csv'
    output_csv = 'processed_malicious_phish2.csv'

    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the column names are correct
    # Replace 'url_column' and 'type_column' with the actual column names in your CSV
    url_column = 'url'
    type_column = 'type'

    # Function to add http if missing
    def add_http_if_missing(url):
        if not url.startswith(('http://', 'https://')):
            return 'http://' + url
        return url

    # Apply the function to all URLs
    df[url_column] = df[url_column].apply(add_http_if_missing)

    # Save the updated DataFrame with both URL and type columns to a new CSV file
    df[[url_column, type_column]].to_csv(output_csv, index=False)

    print(f"Processed CSV saved as '{output_csv}' with URL and type columns.")

def merge_csv():
    # File paths
    original_csv = 'malicious_phish2.csv'
    processed_csv = 'processed_malicious_phish2.csv'

    # Load both CSV files
    df_original = pd.read_csv(original_csv)
    df_processed = pd.read_csv(processed_csv)

    # Concatenate the original and processed data
    df_combined = pd.concat([df_original, df_processed])

    # Drop duplicate rows based on the URL and type columns, keeping the first occurrence
    df_combined = df_combined.drop_duplicates(subset=['url', 'type'], keep='first')

    # Save the merged data back to the original CSV file without duplicates
    df_combined.to_csv(original_csv, index=False)

    print(f"Merged data without duplicates has been saved back to '{original_csv}'.")


def scheme_domain_only():
    # File path for the processed CSV
    processed_csv = 'processed_malicious_phish2.csv'

    # Load the CSV file
    df = pd.read_csv(processed_csv)

    # Ensure the URL column name is correct in the CSV file
    url_column = 'url'

    # Function to extract domain and add http if missing, with error handling
    def extract_domain_with_http(url, index, row_data):
        try:
            parsed_url = urlparse(url)
            # Use only netloc (domain) and scheme; default to http if no scheme
            scheme = parsed_url.scheme if parsed_url.scheme else 'http'
            domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
            return f"{scheme}://{domain}"
        except ValueError:
            # Print the entire row if there is an invalid URL
            print(f"Invalid URL encountered in row {index}:\n{row_data}\n")
            return url  # Optionally return the original URL or replace it with a placeholder

    # Apply the function with row index and row data to each URL in the column
    df[url_column] = [
        extract_domain_with_http(url, idx, df.iloc[idx])
        for idx, url in enumerate(df[url_column])
    ]

    # Save the updated DataFrame to the same CSV file
    df.to_csv(processed_csv, index=False)

    print(f"Updated '{processed_csv}' to include domain only with http or https.")


merge_csv()