import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

# Function to extract all links from a given URL : It specifically
# - Parse the HTML using BeautifulSoup
# - Find all 'a' tags with href attributes
# - Convert relative URLs to absolute URLs

def extract_links_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        full_links = []
        for link in links:
            if link.startswith("mailto:") or link.startswith("javascript:"):
                continue
            full_link = urljoin(url, link)
            full_links.append(full_link)

        return list(set(full_links))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

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
            with open(file_name, 'r') as file:
                return set(line.strip() for line in file if line.strip())
        except IOError as e:
            print(f"Error reading the file {file_name}: {e}")
            return set()
    return set()

# This function : 
# - Loads existing links to avoid duplication
# - Find links that are not already in the file
# - Append the new links to the file

def save_links_to_txt(links, file_name):
    """
    Appends new links to the specified file without duplicates.
    Args:
        links (set): The set of links to save.
        file_name (str): The name of the file to save the links.
    """
    try:
        existing_links = load_existing_links(file_name)
        new_links = links - existing_links

        if new_links:
            with open(file_name, 'a') as file:
                for link in new_links:
                    file.write(link + '\n')
            print(f"Appended {len(new_links)} new links to {file_name}.")
        else:
            print("No new links to append. Everything's already saved!")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    start_url = input("Enter the URL to extract links from: ")
    output_file = "stonybrook_links.txt"

    print("Extracting links... This might take a few seconds.")
    links = extract_links_from_url(start_url)

    if links:
        print(f"Found {len(links)} links!")
        save_links_to_txt(set(links), output_file)
    else:
        print("No links found or an error occurred. Try a different URL!")