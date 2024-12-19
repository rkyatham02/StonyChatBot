# Stonybrook University Chatbot

Stonybrook University Chatbot is an AI-powered assistant designed to answer questions about Stonybrook University's website and the Computer Science bulletin board.

## Table of Contents

- [Introduction](#introduction)
- [Installation/Running](#installation)

## Introduction

Stonybrook University Chatbot is built using AI and natural language processing techniques to provide helpful responses to inquiries about Stonybrook University's website content and the Computer Science bulletin board.

## Installation/Running

To install Stonybrook University Chatbot, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>

2. Navigate to the project directory:

3. Install the dependencies using pip:
pip install -r requirements.txt

4. Go into the code and into env.sh, change the API key into your API key. After changing this, you can also put whatever links you want it to webscrape over for information about the stonybrook website.

I am giving this freedom since respective of your major, you have your own bulletin board so you can put these links into it.
store_docs(Enter link you want to webscrape and embed into the chatbot)

5. Then run the main script by typing in :
streamlit run main.py

After you do these steps, you can ask the chatbot any question you want regarding the website and the website links you gave it