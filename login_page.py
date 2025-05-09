# to do 
# change 'sign-up' button in sign-up page to 'Go to log-in' page button after successfully creating a user info 
# for security puposes, uncomment the lines of password hashing in functions add_user, authenticate_user
# for testing purposes, leave those as it is..

import streamlit as st
import sqlite3
import hashlib
import os

# Create hidden data folder
db_dir = ".data"
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "users.db")

# Connect to SQLite database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add a new user
def add_user(username, name, password):
    # hashed_pw = hash_password(password)
    # c.execute('INSERT INTO users (username, name, password) VALUES (?, ?, ?)', (username, name, hashed_pw))
    c.execute('INSERT INTO users (username, name, password) VALUES (?, ?, ?)', (username, name, password))
    conn.commit()

# Authenticate login
def authenticate_user(username, password):
    # hashed_pw = hash_password(password)
    # c.execute('SELECT name FROM users WHERE username = ? AND password = ?', (username, hashed_pw))
    c.execute('SELECT name FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchone()

# Sign-up page
def display_signup_page():
    st.title("Sign Up")
    new_name = st.text_input("Full Name")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")

    if st.button("Sign Up"):
        if new_username and new_password and new_name:
            try:
                add_user(new_username, new_name, new_password)
                st.success("Account created! You can now log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Choose a different one.")
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
            st.session_state["user_fullname"] = user[0]
            st.success(f"Logged in as {user[0]}")
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






# import streamlit as st

# # Dummy credentials (replace with a database or external auth system in production)
# credentials = {
#     "usernames": {
#         "user1": {"name": "User One", "password": "pass123"},
#         "admin": {"name": "Admin User", "password": "admin456"}
#     }
# }

# # Function to display and handle the login page
# def display_login_page():
#     st.title("Login to Information Retrieval System")
    
#     # Input fields for username and password
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
    
#     # Login button
#     if st.button("Login"):
#         if username in credentials["usernames"] and credentials["usernames"][username]["password"] == password:
#             st.session_state["logged_in"] = True
#             st.session_state["username"] = username
#             st.session_state["user_fullname"] = credentials["usernames"][username]["name"]
#             st.success(f"Logged in as {credentials['usernames'][username]['name']}")
#             st.rerun()  # Refresh the page to show the main app
#         else:
#             st.error("Incorrect username or password")

# # Function to display the main app after login
# def display_main_app():
#     st.title("Welcome to the Information Retrieval System")
#     st.write(f"Hello, {st.session_state['user_fullname']}!")
    
#     # Example placeholder for your app content
#     st.write("This is where your app functionality (Google API, speech features, etc.) would go.")
    
#     # Logout button
#     if st.button("Logout"):
#         st.session_state["logged_in"] = False
#         st.session_state.pop("username", None)
#         st.session_state.pop("user_fullname", None)
#         st.rerun()  # Refresh to return to login page

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False

# # Main app logic
# if not st.session_state["logged_in"]:
#     display_login_page()
# else:
#     display_main_app()







# import streamlit as st

# # Dummy credentials
# credentials = {
#     "usernames": {
#         "user1": {"name": "User One", "password": "pass123"},
#         "admin": {"name": "Admin User", "password": "admin456"}
#     }
# }

# # Login page function
# def display_login_page():
#     st.title("Login Page")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if username in credentials["usernames"] and credentials["usernames"][username]["password"] == password:
#             st.session_state["logged_in"] = True
#             st.session_state["username"] = username
#             st.success(f"Logged in as {credentials['usernames'][username]['name']}")
#             st.rerun()
#         else:
#             st.error("Incorrect username or password")

# # Main app function
# def display_main_app():
#     st.title("Welcome!")
#     st.write(f"Hello, {credentials['usernames'][st.session_state['username']]['name']}!")
#     if st.button("Logout"):
#         st.session_state["logged_in"] = False
#         st.session_state.pop("username", None)
#         st.rerun()

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False

# # App logic
# if not st.session_state["logged_in"]:
#     display_login_page()
# else:
#     display_main_app()