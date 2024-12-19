# Stony Brook University Chatbot

Stony Brook University Chatbot is an AI-powered assistant designed to answer questions about Stony Brook University's website and the Computer Science bulletin board. It leverages natural language processing and web scraping techniques to provide accurate and relevant responses based on the embedded content.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

## Introduction

Stony Brook University Chatbot is a user-friendly virtual assistant tailored for current and prospective students, faculty, and staff. It aims to make navigating and understanding the university’s resources more accessible by answering queries related to the university’s website and bulletin boards.

## Features

- **AI-Powered Assistance**: Provides intelligent answers to user queries using advanced natural language processing.
- **Web Scraping**: Embeds information from user-specified web pages to enhance its knowledge base.
- **Customizable**: Users can specify their own set of links for the chatbot to scrape and learn from.
- **Interactive Interface**: Built using Streamlit for a clean, intuitive, and responsive user experience.

## Installation and Setup

Follow these steps to install and set up the chatbot on your system:

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd stonybrook_chatbot
   ```

3. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set the API Key**:
   Open the `env.sh` file and replace the placeholder API key with your OpenAI API key:
   ```plaintext
   export OPENAI_API_KEY='your_api_key_here'
   ```

5. **Extract Links from the Stony Brook Website**:
   Use `extract_link_from_specific_website.py` to extract all relevant course and bulletin links from the Stony Brook University website:
   ```bash
   python extract_link_from_specific_website.py
   ```

6. **Refine Extracted Links**:
   Once the initial links are gathered, use `json_web_crawler.py` to extract all links from the specified domain:
   ```bash
   python json_web_crawler.py
   ```

7. **Generate Embeddings**:
   Use `embeddings_generator.py` to process the extracted links, delete existing vector store data, and generate new embeddings:
   ```bash
   python embeddings_generator.py
   ```

   - This script loads the `documents.json` file, processes the URLs, and stores embeddings.
   - Errors during processing are logged in `error_log.txt`.

8. **Run the Chatbot**:
   Launch the application using Streamlit:
   ```bash
   streamlit run main.py
   ```

## Usage

Once the application is running, follow these steps:

1. Open the provided local URL (e.g., `http://localhost:8501`) in your web browser.
2. Log in or sign up to access the chatbot interface.
3. Enter your questions in the text input field, and the chatbot will provide intelligent responses based on the scraped content and pre-embedded knowledge.
4. Use the logout option in the sidebar to end your session securely.

## Customization

- **Modify Web Scraping Links**:
  To scrape additional or different web pages, edit the `store_docs` function in the code.
- **Add Custom Features**:
  Extend the chatbot’s functionality by modifying the `helper_functions.py` file or other related modules.

## Troubleshooting

If you encounter issues, refer to the following tips:

- **OPENAI_API_KEY Error**:
  Ensure the API key is correctly set in your environment or `.env` file. Verify it using:
  ```python
  import os
  print(os.getenv("OPENAI_API_KEY"))
  ```

- **Dependency Errors**:
  Reinstall the dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

- **Login Issues**:
  Check if Firebase is correctly configured and the `firebase_key.json` file is in the project directory.