import os
import json
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from helper_functions import store_docs, is_url_valid

load_dotenv('../env.sh')

def delete_data_file():
    try:
        os.remove("data/chroma/vector_store.json")
    except FileNotFoundError:
        pass

def load_document_urls(file_path="documents.json"):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data.get("urls", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading URLs from {file_path}: {e}")
        return []

def main():
    """Processes document URLs and stores embeddings."""
    delete_data_file() 
    document_urls = load_document_urls()
    error_log_file = "error_log.txt"

    print("Storing documents into the vector store... Hang tight! 🚀")
    with open(error_log_file, "a", encoding="utf-8") as error_file:
        for url in tqdm(document_urls, desc="Processing URLs"):
            if is_url_valid(url):
                try:
                    store_docs(url)
                except Exception as e:
                    error_message = f"Error processing {url}: {e}"
                    error_file.write(error_message + "\n")
                    print(error_message)
            else:
                error_message = f"Skipping invalid URL: {url}"
                error_file.write(error_message + "\n")
                print(error_message)

if __name__ == "__main__":
    main()
