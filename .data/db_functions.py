import streamlit as st
from supabase import create_client
import hashlib

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

DEBUG = True

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add a new user
def add_user(username, name, password):
    if not DEBUG:
        password = hash_password(password)
    data = {
        "username": username,
        "name": name,
        "password": password
    }
    res = supabase.table("users").insert(data).execute()
    return res

# Authenticate login
def authenticate_user(username, password):
    if not DEBUG:
        password = hash_password(password)
    res = supabase.table("users").select("name").eq("username", username).eq("password", password).execute()
    if res.data:
        return res.data[0]["name"]
    return None

# Sign-up page
def display_signup_page():
    st.title("Sign Up")
    new_name = st.text_input("Full Name")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")

    if st.button("Sign Up"):
        if new_username and new_password and new_name:
            # Check if username already exists
            existing_user = supabase.table("users").select("id").eq("username", new_username).execute()
            if existing_user.data:
                st.error("Username already exists. Choose a different one.")
            else:
                res = add_user(new_username, new_name, new_password)
                if res.data:
                    st.success("Account created! You can now log in.")
                else:
                    st.error("Signup failed.")
                    if DEBUG:
                        st.json(res.model_dump())  # Show raw error for debugging
        else:
            st.warning("Please fill all fields.")

# Login page
def display_login_page():
    st.title("Login to Information Retrieval System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["user_fullname"] = user
            st.success(f"Logged in as {user}")
            st.rerun()
        else:
            st.error("Incorrect username or password")

# Main app after login
def display_main_app():
    st.title("Welcome to the Information Retrieval System")
    st.write(f"Hello, {st.session_state['user_fullname']}!")

    st.write("This is where your app functionality goes.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# Session and menu control
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"] if not st.session_state["logged_in"] else ["Home"])

if not st.session_state["logged_in"]:
    if menu == "Login":
        display_login_page()
    else:
        display_signup_page()
else:
    display_main_app()
