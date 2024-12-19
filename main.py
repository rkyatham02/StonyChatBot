import os
from dotenv import load_dotenv
import streamlit as st
from helper_functions import get_response

# Load environment variables
load_dotenv()  # Load variables from a .env file in the current directory

# Verify if the OpenAI API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set. Please set it in your .env file or environment variables.")

# Define the Streamlit app
def main():
    """
    Defines the Streamlit UI for the Stony Brook University chatbot.
    """
    # Title and description
    st.title("Stony Brook University Chatbot 🎓")
    st.markdown(
        "<p style='font-size: 18px;'>Welcome to the Stony Brook University chatbot. Ask me anything!</p>",
        unsafe_allow_html=True,
    )

    # User input field
    user_question = st.text_input("Ask a question:")

    # Button to submit the question
    if st.button("Ask"):
        try:
            # Get response from the chatbot
            response = get_response(user_question, university_name, university_info, univ_useful_links)
            # Display the response
            st.markdown(f"<p style='font-weight: bold;'>Answer:</p> {response}", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Something went wrong while fetching the response: {e}")

    # Stony Brook University image
    st.image("images/stonybrook_univ_image.png", caption="Stony Brook University", width=400)

# Setting up organization information
university_name = "Stony Brook University"
university_info = (
    "Stony Brook University is a public research university located in Stony Brook, New York. "
    "It offers a wide range of undergraduate and graduate programs across various fields, including "
    "arts, sciences, engineering, medicine, and business."
)
univ_useful_links = """Email: admissions@stonybrook.edu
Phone: +1 (631) 632-6000
Admissions: https://www.stonybrook.edu/undergraduate-admissions/
Graduate Admissions: https://www.stonybrook.edu/graduate-admissions/
Financial Aid: https://www.stonybrook.edu/commcms/finaid/
Campus Map: https://www.stonybrook.edu/commcms/admissions/visit/campus-map
Student Portal: https://www.stonybrook.edu/estudent/
CS Graduation Track: https://www.stonybrook.edu/sb/bulletin/current/academicprograms/cse/degreesandrequirements.php"""

if __name__ == "__main__":
    main()
