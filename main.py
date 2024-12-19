import os
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
from helper_functions import get_response

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY is not set. Please set it in your .env file or environment variables.")

firebase_key_path = "firebase_key.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_app = firebase_admin.initialize_app(cred)

def firebase_create_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return None

def firebase_sign_in(email, password):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        st.error(f"Error signing in: {e}")
        return None
    
def login():
    st.title("Login to Stony Brook Chatbot 🎓")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = firebase_sign_in(email, password)
        if user_id:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
            st.success("Login successful!")
            st.session_state["page"] = "chatbot"

def signup():
    st.title("Sign Up for Stony Brook Chatbot 🎓")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        user_id = firebase_create_user(email, password)
        if user_id:
            st.success("Account created successfully! Please log in.")
            st.session_state["page"] = "login"

def chatbot_app():
    st.title("Stony Brook University Chatbot 🎓")
    st.markdown("Welcome to the Stony Brook University chatbot. Ask me anything!")
    user_question = st.text_input("Ask a question:")
    if st.button("Ask"):
        try:
            response = get_response(user_question, university_name, university_info, univ_useful_links)
            st.markdown(f"**Answer:** {response}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    st.image("images/stonybrook_univ_image.png", caption="Stony Brook University", width=400)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if not st.session_state["logged_in"]:
        if st.session_state["page"] == "login":
            login()
        elif st.session_state["page"] == "signup":
            signup()
        st.sidebar.button("Go to Signup", on_click=lambda: st.session_state.update({"page": "signup"}))
        st.sidebar.button("Go to Login", on_click=lambda: st.session_state.update({"page": "login"}))
    else:
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "page": "login"}))
        chatbot_app()

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
