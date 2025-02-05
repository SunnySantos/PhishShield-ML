import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):
    suspicious_keywords = ['verify', 'secure', 'account', 'update', 'confirm', 'payment', 'wallet', 'wallets']
    shortening_services = ['bit.ly', 'goo.gl', 't.co', 'tinyurl.com', 'ow.ly']
    suspicious_tlds = ['.xyz', '.top', '.club', '.info']

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Feature 1: Length of URL
    url_length = len(url)

    # Feature 2: Number of slashes
    num_slashes = url.count('/')

    # Feature 3: HTTPS check
    use_https = 1 if url.startswith('https') else 0

    # Feature 4: Number of digits in the entire URL
    num_digits = sum(c.isdigit() for c in url)

    # Feature 5: Number of periods ('.') in the URL
    num_periods = url.count('.')

    # Feature 6: Query parameter count
    query_params_count = len(re.findall(r'\?.*$', url))

    # Feature 7: Subdomain count
    domain_parts = tldextract.extract(url).subdomain
    num_subdomains = len(domain_parts) - 2 if len(domain_parts) > 2 else 0

    # Feature 8: Multiple subdomains (more than 1)
    has_multiple_subdomains = 1 if num_subdomains > 1 else 0

    # Feature 9: Presence of special characters
    special_chars = any(char in url for char in ['@', '-', '_', '&', '%', '$', '#', '?', '!', '+'])
    presence_of_special_chars = 1 if special_chars else 0

    # Feature 10: IP address detection
    contains_ip_address = int(bool(re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', url)))

    # Feature 11: Suspicious keyword presence
    contains_suspicious_keyword = int(any(keyword in url.lower() for keyword in suspicious_keywords))

    # Feature 12: Uses shortening service
    uses_shortening_service = int(any(service in domain for service in shortening_services))

    # Feature 13: Suspicious TLD check
    uses_suspicious_tld = int(any(tldextract.extract(url).suffix for tld in suspicious_tlds))

    # Feature 14: Domain contains more than 5 digits
    total_digits_in_domain = sum(c.isdigit() for c in domain)
    contains_more_than_5_digits = 1 if total_digits_in_domain > 5 else 0

    # Feature 15: Punycode detection
    is_punycode = 1 if domain.startswith('xn--') else 0

    # Collect all extracted features
    features = [
        url_length, num_slashes, use_https, num_digits, num_periods,
        query_params_count, num_subdomains, has_multiple_subdomains,
        presence_of_special_chars, contains_ip_address,
        contains_suspicious_keyword, uses_shortening_service,
        uses_suspicious_tld, contains_more_than_5_digits,
        is_punycode
    ]

    # print('No. of Slashes:', num_slashes)
    # print('Is using HTTPS', use_https)
    # print('No. of digits', num_digits)
    # print('No. of periods', num_periods)
    # print('No. of query parameters', query_params_count)
    # print('No. of subdomains', num_subdomains)
    # print('Has multiple subdomains', has_multiple_subdomains)
    # print('Special Characters', presence_of_special_chars)
    # print('Contains IP Address', contains_ip_address)
    # print('Contains suspicious keywords', contains_suspicious_keyword)
    # print('Uses shortening service', uses_shortening_service)
    # print('Uses suspicious Top Level Domain', uses_suspicious_tld)
    # print('Contains more then 5 digits', contains_more_than_5_digits)
    # print('Is punycode', is_punycode) 

    return features
