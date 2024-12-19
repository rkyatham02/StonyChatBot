import os
import json
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from helper_functions import store_docs, is_url_valid

# Load the OPENAI KEY from the env.sh file
load_dotenv('../env.sh')

# Function to delete the existing data file
def delete_data_file():
    """Deletes the existing vector store file to start fresh."""
    try:
        os.remove("data/chroma/vector_store.json")  # Deletes old data
    except FileNotFoundError:
        pass  # File doesn't exist? No problem.

# Function to load URLs from a configuration file
def load_document_urls(file_path="documents.json"):
    """
    Reads the URLs from a JSON file.
    Args:
        file_path (str): Path to the JSON file.
    Returns:
        list: A list of URLs to process.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data.get("urls", [])  # Return the list of URLs or an empty list
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading URLs from {file_path}: {e}")
        return []

# Main function to process URLs and store embeddings
def main():
    """Processes document URLs and stores embeddings."""
    delete_data_file()  # Optional: Delete the existing vector store

    # Load document URLs
    document_urls = load_document_urls()

    # Error log file
    error_log_file = "error_log.txt"

    # Progress bar for storing webpage content
    print("Storing documents into the vector store... Hang tight! 🚀")
    with open(error_log_file, "a", encoding="utf-8") as error_file:  # Log errors to a file with UTF-8 encoding
        for url in tqdm(document_urls, desc="Processing URLs"):
            if is_url_valid(url):  # Check if the URL is valid
                try:
                    store_docs(url)  # Process each URL
                except Exception as e:
                    error_message = f"Error processing {url}: {e}"
                    error_file.write(error_message + "\n")
                    print(error_message)  # Log to console and file
            else:
                error_message = f"Skipping invalid URL: {url}"
                error_file.write(error_message + "\n")
                print(error_message)

if __name__ == "__main__":
    main()
