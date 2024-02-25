
# Functions for User Management

def authenticate(username, password):
    try:
        with open("users.txt", "r") as file: # Opens the users.txt file
            for user in file: # Loop going to all users to find the speific user we are trying to login
                user_data = user.strip().split(',') # Splitting the "," from the data
                if user_data[0] == username and user_data[1] == password: # If the username and password are same in users.txt it will return true
                    return True
    except FileNotFoundError:
        print("Error: Users file not found.")
    return False

def add_user(new_username, new_password, new_role):
    with open("users.txt", "a") as file:
        file.write(f"{new_username},{new_password},{new_role}\n")
    print(f"Added new user: {new_username}, Role: {new_role}")


def change_user_details():
    username = input("Enter the username of the user whose details you want to change: ")
    with open("users.txt", "r") as file:
        users = file.readlines()
    found = False
    updated_users = []
    for user in users:
        user_data = user.strip().split(',')
        if user_data[0] == username:
            found = True
            new_username = input("Enter new username (leave empty to keep current): ")
            new_password = input("Enter new password (leave empty to keep current): ")
            new_role = input("Enter new role (leave empty to keep current): ")
            if not new_username:
                new_username = user_data[0]
            if not new_password:
                new_password = user_data[1]
            if not new_role:
                new_role = user_data[2]
            updated_users.append(f"{new_username},{new_password},{new_role}\n")
            print("User details updated.")
        else:
            updated_users.append(user)
    if not found:
        print("User not found.")
    else:
        with open("users.txt", "w") as file:
            file.writelines(updated_users)


# Functions for Menu Management

def update_menu():
    print("1. Update existing menu item")
    print("2. Add a new menu item")
    print("3. View menu items")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        update_existing_menu_item()
    elif choice == "2":
        add_new_menu_item()
    elif choice == "3":
        view_all_menu_items()
    elif choice == "4":
        manager_interface()
    else:
        print("Invalid choice. Please try again.")

def update_existing_menu_item():
    item_name = input("Enter the name of the menu item to update: ")
    new_price = input("Enter the new price for the menu item: ")
    
    menu_items = read_menu_items()
    if item_name in menu_items:
        menu_items[item_name] = new_price
        write_menu_items(menu_items)
        print(f"Updated menu item: {item_name} - New Price: {new_price}")
    else:
        print("Menu item not found.")

def add_new_menu_item():
    item_name = input("Enter the name of the new menu item: ")
    price = input("Enter the price for the new menu item: ")
    
    menu_items = read_menu_items()
    if item_name not in menu_items:
        menu_items[item_name] = price
        write_menu_items(menu_items)
        print(f"Added new menu item: {item_name} - Price: {price}")
    else:
        print("Menu item already exists.")
        
    manager_interface()

def block_cancel_food_item():
    item_name = input("Enter the name of the food item to manage: ")
    menu_items = read_menu_items()
    
    if item_name in menu_items:
        print("Select action:")
        print("1. Block")
        print("2. Cancel")
        print("3. Reactivate (Make active)")
        action_option = input("Enter your choice (1, 2, or 3): ")

        if action_option == "1":
            menu_items[item_name]["status"] = "blocked"
            print(f"Food item {item_name} blocked.")
        elif action_option == "2":
            menu_items[item_name]["status"] = "cancelled"
            print(f"Food item {item_name} cancelled.")
        elif action_option == "3":
            menu_items[item_name]["status"] = "active"
            print(f"Food item {item_name} reactivated.")
        else:
            print("Invalid choice.")
        
        write_menu_items(menu_items)
    else:
        print(f"Food item {item_name} not found in the menu.")

    # Return to the manager interface
    manager_interface()


def read_menu_items():
    try:
        with open("menu.txt", "r") as file:
            menu_items = {}
            for line in file:
                item_data = line.strip().split(',')
                item_name = item_data[0]
                price = float(item_data[1])
                status = item_data[2] if len(item_data) == 3 else "active"
                menu_items[item_name] = {"price": price, "status": status}
        return menu_items
    except FileNotFoundError:
        return {}


def write_menu_items(menu_items):
    with open("menu.txt", "w") as file:
        for item_name, data in menu_items.items():
            status = data.get("status", "active")
            file.write(f"{item_name},{data['price']},{status}\n")
    print("Menu items updated successfully.")


def view_all_menu_items():
    menu_items = read_menu_items()
    if menu_items:
        print("All Menu Items:")
        for item_name, data in menu_items.items():
            price = data["price"]
            status = data["status"]
            print(f"{item_name}: Price: {price}, Status: {status}")
    else:
        print("The menu is currently empty.")




# Function for the table managemnt
        
def update_tables():
    print("1. Add/Update table")
    print("2. Show available tables")
    print("3. Change status of a table")
    print("4. Exit")
    choice = input("Enter your choice: ")


    if choice == "1":
        add_update_table()
    elif choice == "2":
        show_available_tables()
    elif choice == "3":
        change_table_status()
    elif choice == "4":
        manager_interface()
    else:
        print("Invalid choice. Please try again.")

def add_update_table():
    table_number = input("Enter table number: ")
    capacity = input("Enter capacity for the table: ")
    
    tables = read_tables()
    tables[table_number] = capacity
    write_tables(tables)
    print(f"Added/Updated table: Table {table_number} - Capacity: {capacity}")

    # Return to the manager interface
    manager_interface()

def change_table_status():
    table_number = input("Enter the table number to change status: ")
    new_status = input("Enter new status (available/not available): ")

    tables = read_tables()
    if table_number in tables:
        tables[table_number] = new_status
        write_tables(tables)
        print(f"Status of table {table_number} changed to: {new_status}")
    else:
        print("Table not found.")

    # Return to the manager interface
    manager_interface()

def change_table_status():
    table_number = input("Enter the table number to change status: ")
    print("Select status:")
    print("1. Available")
    print("2. Not Available")
    new_status_option = input("Enter your choice (1 or 2): ")

    new_status = "available" if new_status_option == "1" else "not available"

    tables = read_tables()
    if table_number in tables:
        tables[table_number] = new_status
        write_tables(tables)
        print(f"Status of table {table_number} changed to: {new_status}")
    else:
        print("Table not found.")

    # Return to the manager interface
    manager_interface()

def show_available_tables():
    tables = read_tables()
    if tables:
        print("Available Tables:")
        for table, status in tables.items():
            if status == "available":
                print(f"Table {table}: Status - {status}")
    else:
        print("No tables are available at the moment.")
def read_tables():
    try:
        with open("tables.txt", "r") as file:
            tables = {}
            for line in file:
                table_number, status = line.strip().split(',')
                tables[table_number] = status
        return tables
    except FileNotFoundError:
        return {}

def write_tables(tables):
    with open("tables.txt", "w") as file:
        for table_number, status in tables.items():
            file.write(f"{table_number},{status}\n")
    print("Tables updated successfully.")

# Functions for Manager Operations

def manager_interface():
    while True:
        print("\nManager Interface:")
        print("1. Add new user")
        print("2. Update user details")
        print("3. Add/View/Update menu item")
        print("4. Add/View/Update table")
        print("5. Cancel order for specific food item")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            new_role = input("Enter new role: ")
            add_user(new_username, new_password, new_role)
        elif choice == "2":
            change_user_details()
        elif choice == "3":
            update_menu()
        elif choice == "4":
            update_tables()
        elif choice == "5":
            block_cancel_food_item()
        elif choice == "6":
            print("Exiting Manager Interface.")
            break
        else:
            print("Invalid choice. Please try again.")

# Main Program

def main():
    username_input = input("Enter your username: ")
    password_input = input("Enter your password: ")

    if authenticate(username_input, password_input):
        print("Authentication successful.")

        with open("users.txt", "r") as file:
            for user in file: # get the users from users.txt
                user_data = user.strip().split(',') # remvoe "," from users.txt
                if user_data[0] == username_input: # Get the username from users.txt
                    role = user_data[2] # Get the role from users.txt file
                    print(f"Welcome, {role.capitalize()}!")
                    if role == "manager":
                        manager_interface()
                    elif role == "chef":
                        print("This interface is for chef employees.")
                    elif role == "cashier":
                        print("This interface is for cashier employees.")
                    elif role == "waitress":
                        print("This interface is for waitress employees.")
                    else:
                        print(f"Welcome, {role.capitalize()}!")
                    break
    else:
        print("Authentication failed. Please try again.")

if __name__ == "__main__":
    main()
