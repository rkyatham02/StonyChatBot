import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

# Function to extract all links from a given URL
def extract_links_from_url(url):
    """
    Extracts all links from the webpage at the given URL.
    Args:
        url (str): The URL to extract links from.
    Returns:
        list: A list of unique links found on the page.
    """
    try:
        # Step 1: Get the HTML content of the webpage
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Step 2: Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Find all 'a' tags with href attributes
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Step 4: Convert relative URLs to absolute URLs
        full_links = []
        for link in links:
            # Skip unwanted links (like mailto or JavaScript)
            if link.startswith("mailto:") or link.startswith("javascript:"):
                continue
            full_link = urljoin(url, link)
            full_links.append(full_link)

        # Remove duplicates and return as a list
        return list(set(full_links))
    except requests.exceptions.RequestException as e:
        # Handle any errors during the request
        print(f"Error fetching URL {url}: {e}")
        return []

# Function to load existing links from the file
def load_existing_links(file_name):
    """
    Loads existing links from the specified file.
    Args:
        file_name (str): Name of the file to read from.
    Returns:
        set: A set of links already saved in the file.
    """
    if os.path.exists(file_name):
        try:
            # Open the file and read all lines
            with open(file_name, 'r') as file:
                # Use a set to avoid duplicates
                return set(line.strip() for line in file if line.strip())
        except IOError as e:
            # Handle file read errors
            print(f"Error reading the file {file_name}: {e}")
            return set()
    return set()

# Function to save new links to a file
def save_links_to_txt(links, file_name):
    """
    Appends new links to the specified file without duplicates.
    Args:
        links (set): The set of links to save.
        file_name (str): The name of the file to save the links.
    """
    try:
        # Step 1: Load existing links to avoid duplication
        existing_links = load_existing_links(file_name)

        # Step 2: Find links that are not already in the file
        new_links = links - existing_links

        # Step 3: Append the new links to the file
        if new_links:
            with open(file_name, 'a') as file:
                for link in new_links:
                    file.write(link + '\n')  # Add each new link to a new line
            print(f"Appended {len(new_links)} new links to {file_name}.")
        else:
            print("No new links to append. Everything's already saved!")
    except IOError as e:
        # Handle file write errors
        print(f"Error writing to file: {e}")

# Main script logic
if __name__ == "__main__":
    # Ask the user for the URL to scrape
    start_url = input("Enter the URL to extract links from: ")
    output_file = "stonybrook_links.txt"  # File to store all links

    # Step 1: Extract links from the provided URL
    print("Extracting links... This might take a few seconds.")
    links = extract_links_from_url(start_url)

    # Step 2: Save the extracted links to the file
    if links:
        print(f"Found {len(links)} links!")
        save_links_to_txt(set(links), output_file)  # Use a set to remove duplicates
    else:
        print("No links found or an error occurred. Try a different URL!")