import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
from tqdm import tqdm  # For progress tracking

# Function to extract all the links from a URL, limited to the same domain
def extract_links_from_url(url, domain):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        domain_links = []
        for link in links:
            if link.startswith("mailto:") or link.startswith("javascript:"):
                continue
            full_link = urljoin(url, link)
            if domain in urlparse(full_link).netloc:
                domain_links.append(full_link)

        return list(set(domain_links))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

def load_existing_links(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                return set(data.get("urls", []))
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading the file {file_name}: {e}")
            return set()
    return set()

def save_links_to_json(links, file_name):
    data = {"urls": list(links)}
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Links saved to {file_name}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def read_urls_from_txt(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except IOError as e:
        print(f"Error reading the file {file_name}: {e}")
        return []

if __name__ == "__main__":
    input_file = input("Enter the path to the .txt file with URLs: ")
    file_name = "documents.json"

    urls = read_urls_from_txt(input_file)

    if not urls:
        print("No URLs found in the input file.")
        exit()

    existing_links = load_existing_links(file_name)
    print("Extracting links from the URLs. Hang tight...")
    for start_url in tqdm(urls, desc="Processing URLs"):
        domain = urlparse(start_url).netloc
        new_links = extract_links_from_url(start_url, domain)
        existing_links.update(new_links)

    save_links_to_json(existing_links, file_name)
    print(f"Processing complete. Total links in JSON: {len(existing_links)}")