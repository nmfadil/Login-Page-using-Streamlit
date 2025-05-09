import sqlite3

DB_PATH = "users.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def print_users_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if users:
        print("\nRegistered Users:\n")
        print("{:<15} {:<20} {:<20}".format("Username", "Full Name", "Password"))
        print("-" * 60)
        for user in users:
            print("{:<15} {:<20} {:<20}".format(user[0], user[1], user[2]))
    else:
        print("No users found.")

    conn.close()

def search_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        print("\nUser found:")
        print(f"Username: {user[0]}")
        print(f"Full Name: {user[1]}")
        print(f"Password: {user[2]}")
    else:
        print(f"\nUser '{username}' not found.")

    conn.close()

def delete_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print(f"\nUser '{username}' does not exist.")
    else:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print(f"\nUser '{username}' deleted.")

    conn.close()

# --- Menu for terminal use ---
if __name__ == "__main__":
    while True:
        print("\n--- User Database Menu ---")
        print("1. View all users")
        print("2. Search for a user")
        print("3. Delete a user")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            print_users_table()
        elif choice == "2":
            username = input("Enter username to search: ").strip()
            search_user(username)
        elif choice == "3":
            username = input("Enter username to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").strip().lower()
            if confirm == "y":
                delete_user(username)
            else:
                print("Deletion cancelled.")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1-4.")





# import sqlite3

# # Path to your database
# DB_PATH = "users.db"

# def print_users_table():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Confirm the table exists
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
#     if cursor.fetchone():
#         cursor.execute("SELECT * FROM users")
#         users = cursor.fetchall()

#         if users:
#             print("\nRegistered Users:\n")
#             print("{:<15} {:<20} {:<20}".format("Username", "Full Name", "Password"))
#             print("-" * 60)
#             for user in users:
#                 print("{:<15} {:<20} {:<20}".format(user[0], user[1], user[2]))
#         else:
#             print("No users found.")
#     else:
#         print("Table 'users' does not exist.")

#     conn.close()

# if __name__ == "__main__":
#     print_users_table()
