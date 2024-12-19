import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
from tqdm import tqdm  # For progress tracking

# Function to extract all the links from a URL, limited to the same domain
def extract_links_from_url(url, domain):
    """
    Extracts links from the given URL, restricted to the specified domain.
    Args:
        url (str): The URL to scrape links from.
        domain (str): The domain to filter the links.
    Returns:
        list: A list of unique links within the same domain.
    """
    try:
        # Step 1: Fetch the webpage content
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Throws an error for bad HTTP responses

        # Step 2: Parse the webpage content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Get all 'a' tags with href attributes
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Step 4: Normalize links and filter by the domain
        domain_links = []
        for link in links:
            # Ignore weird links like mailto or JavaScript
            if link.startswith("mailto:") or link.startswith("javascript:"):
                continue
            # Convert relative links to full links
            full_link = urljoin(url, link)
            # Check if the link belongs to the same domain
            if domain in urlparse(full_link).netloc:
                domain_links.append(full_link)

        # Return the unique links
        return list(set(domain_links))
    except requests.exceptions.RequestException as e:
        # Oops, something went wrong with the request
        print(f"Error fetching URL {url}: {e}")
        return []

# Function to load existing links from a JSON file
def load_existing_links(file_name):
    """
    Loads existing links from a JSON file, if it exists.
    Args:
        file_name (str): The name of the JSON file.
    Returns:
        set: A set of links already saved in the file.
    """
    if os.path.exists(file_name):
        try:
            # Read the file and load as JSON
            with open(file_name, 'r') as file:
                data = json.load(file)
                return set(data.get("urls", []))  # Return the set of links
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading the file {file_name}: {e}")
            return set()
    return set()  # If the file doesn't exist, return an empty set

# Function to save links to a JSON file
def save_links_to_json(links, file_name):
    """
    Saves the updated links to a JSON file.
    Args:
        links (set): A set of links to save.
        file_name (str): The name of the JSON file.
    """
    data = {"urls": list(links)}  # Convert the set to a list for JSON
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)  # Pretty print with indent
        print(f"Links saved to {file_name}")
    except IOError as e:
        # Handle file write errors
        print(f"Error writing to file: {e}")

# Function to read URLs line by line from a text file
def read_urls_from_txt(file_name):
    """
    Reads URLs from a text file, one per line.
    Args:
        file_name (str): The name of the text file.
    Returns:
        list: A list of URLs from the file.
    """
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except IOError as e:
        print(f"Error reading the file {file_name}: {e}")
        return []

# Main program logic
if __name__ == "__main__":
    # Get the file containing the URLs
    input_file = input("Enter the path to the .txt file with URLs: ")
    file_name = "documents.json"  # File to store the links

    # Step 1: Read URLs from the input file
    urls = read_urls_from_txt(input_file)

    # Exit if no URLs are found
    if not urls:
        print("No URLs found in the input file.")
        exit()

    # Step 2: Load existing links from the JSON file
    existing_links = load_existing_links(file_name)

    # Step 3: Extract links for each URL in the .txt file
    print("Extracting links from the URLs. Hang tight...")
    for start_url in tqdm(urls, desc="Processing URLs"):
        # Extract the domain from the URL
        domain = urlparse(start_url).netloc

        # Extract new links from the URL
        new_links = extract_links_from_url(start_url, domain)

        # Combine new links with the existing ones
        existing_links.update(new_links)

    # Step 4: Save all combined links to the JSON file
    save_links_to_json(existing_links, file_name)

    # Final message
    print(f"Processing complete. Total links in JSON: {len(existing_links)}")