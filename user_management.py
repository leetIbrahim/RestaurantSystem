# user_management.py
import menu_table_management as mtm
import waiter_services
import chef_services
import cashier_services

def authenticate_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        with open('data/users.txt', 'r') as file:
            for line in file:
                user_id, user_name, role, user_password = line.strip().split(',')
                if user_name == username and user_password == password:
                    return role
        print("Authentication failed. Please check your credentials.")
    except FileNotFoundError:
        print("User data file not found. Please ensure the 'data/users.txt' file exists.")
    return None


def show_all_users():
    print("All Users:")
    try:
        with open('data/users.txt', 'r') as file:
            for line in file:
                # Assuming the structure is userID,username,role,password
                user_id, username, role, _ = line.strip().split(',')
                print(f"UserID: {user_id}, Username: {username}, Role: {role}")
    except FileNotFoundError:
        print("Users file not found. Please ensure the 'data/users.txt' file exists.")


def read_users():
    users = []
    try:
        with open('data/users.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:  # Ensures the line has the correct number of elements
                    users.append({'userID': parts[0], 'username': parts[1], 'role': parts[2], 'password': parts[3]})
    except FileNotFoundError:
        print("User file not found. Creating a new one...")
        open('data/users.txt', 'w').close()  # Creates the file if it doesn't exist
    return users

def write_users(users):
    with open('data/users.txt', 'w') as f:
        for user in users:
            f.write(','.join([user['userID'], user['username'], user['role'], user['password']]) + '\n')

def create_user():
    userID = input("Enter user ID: ")
    username = input("Enter username: ")
    role = input("Enter role (manager, chef, cashier, waitress): ")
    password = input("Enter password: ")
    users = read_users()
    users.append({'userID': userID, 'username': username, 'role': role, 'password': password})
    write_users(users)
    print("User created successfully.")

def assign_user_role():
    userID = input("Enter user ID to assign role: ")
    new_role = input("Enter new role (manager, chef, cashier, waitress): ")
    users = read_users()
    for user in users:
        if user['userID'] == userID:
            user['role'] = new_role
            write_users(users)
            print("User role updated successfully.")
            return
    print("User not found.")

def update_user_details():
    userID = input("Enter user ID to update details: ")
    new_username = input("Enter new username: ")
    users = read_users()
    for user in users:
        if user['userID'] == userID:
            user['username'] = new_username
            write_users(users)
            print("User details updated successfully.")
            return
    print("User not found.")

def change_password():
    userID = input("Enter user ID to change password: ")
    new_password = input("Enter new password: ")
    users = read_users()
    for user in users:
        if user['userID'] == userID:
            user['password'] = new_password
            write_users(users)
            print("Password changed successfully.")
            return
    print("User not found.")

def main_menu():
    while True:
        print("\n╔══════════════════════════════╗")
        print("║         Main Menu            ║")
        print("╠══════════════════════════════╣")
        print("║ 1. User Management           ║")
        print("║ 2. Menu and Table Management ║")
        print("║ 3. Exit                      ║")
        print("╚══════════════════════════════╝")
        choice = input("\nEnter your choice (1-3): ")


        if choice == '1':
            user_management_menu()
        elif choice == '2':
            manager_interface()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

def user_management_menu():
    while True:
        print("\n╔══════════════════════════════╗")
        print("║      User Management         ║")
        print("╠══════════════════════════════╣")
        print("║ 1. Show all users            ║")
        print("║ 2. Create User               ║")
        print("║ 3. Assign User Role          ║")
        print("║ 4. Update User Details       ║")
        print("║ 5. Change Password           ║")
        print("║ 6. Return to Main Menu       ║")
        print("╚══════════════════════════════╝")
        choice = input("\nEnter your choice (1-6): ")


        if choice == '1':
            show_all_users()
        elif choice == '2':
            create_user()
        elif choice == '3':
            assign_user_role()
        elif choice == '4':
            update_user_details()
        elif choice == '5':
            change_password()
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

def manager_interface():
    while True:
        print("\n╔════════════════════════════╗")
        print("║   Menu and Table Management║")
        print("╠════════════════════════════╣")
        print("║ 1. Add Menu Item           ║")
        print("║ 2. Update Menu Item        ║")
        print("║ 3. Add Table               ║")
        print("║ 4. Update Table            ║")
        print("║ 5. Show Available Tables   ║")
        print("║ 6. Specify Table Pax       ║")
        print("║ 7. Cancel or Block Order   ║")
        print("║ 8. Return to Main Menu     ║")
        print("╚════════════════════════════╝")
        choice = input("\nEnter your choice (1-8): ")


        if choice == '1':
            mtm.add_menu_item()
        elif choice == '2':
            mtm.update_menu_item()
        elif choice == '3':
            mtm.add_table()
        elif choice == '4':
            mtm.update_table()
        elif choice == '5':
            mtm.show_available_tables()
        elif choice == '6':
            mtm.specify_table_pax()
        elif choice == '7':
            mtm.cancel_block_order()
        elif choice == '8':
            break
        else:
            print("Invalid choice, please try again.")

def main():
    role = authenticate_user()
    if role:
        if role == "manager":
            main_menu()
        elif role == "chef":
            chef_services.chef_interface()
        elif role == "cashier":
            cashier_services.cashier_interface()
        elif role == "waiter":
            waiter_services.waiter_interface()
        else:
            print("Unknown role. Exiting.")

if __name__ == "__main__":
    main()

