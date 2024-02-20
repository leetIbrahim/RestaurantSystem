import json

class Menu:
    def __init__(self):
        self.menu = {}

class Roles:
    def __init__(self):
        self.users_role = {}

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def authenticate(self, username, password):
        return self.username == username and self.password == password

    def get_role(self):
        return self.role

    def update_details(self, new_username, new_role):
        self.username = new_username
        self.role = new_role

    def change_password(self, new_password):
        self.password = new_password

    def __str__(self):
        return f"Username: {self.username}, Role: {self.role}"

class Manager(User):
    def __init__(self, username, password):
        super().__init__(username, password, "manager")
        self.menu = {}
        self.users_role = {}
        self.tables = {}  # Table number: Number of pax
        self.users = {}   # Username: User object
        self.menu_db = "menu.json"  # JSON file for storing menu items
        self.role_db = "users.json"  # JSON file for storing user roles
############################################################
    def add_user(self, new_username, new_password, new_role):
        self.load_users()
        # Add new user to the system
        new_user = User(new_username, new_password, new_role)
        self.users[new_username] = new_user
        # Add user details to users_role dictionary
        self.users_role[new_username] = {"password": new_password, "role": new_role}
        print(f"Added new user: {new_user}")
        self.save_users_role()


    def view_all_users(self):
        # Load existing user roles
        self.load_users()

        if not self.users_role:
            print("No users found.")
            return

        # View all users and their details
        print("All Users:")
        for username, user_info in self.users_role.items():
            print(f"Username: {username}, Password: {user_info['password']}, Role: {user_info['role']}")

    def load_users(self):
        # Load the users from the JSON file into the user dictionary
        try:
            with open(self.role_db, "r") as file:
                data = file.read()
                if data.strip():  # Check if the file is not empty
                    user_list = json.loads(data)
                    # Convert the list of dictionaries back to a dictionary
                    self.users_role = {user['user']: {"password": user['password'], "role": user['role']} for user in user_list}
                else:
                    self.users_role = {}  # Initialize to empty dictionary if file is empty
        except FileNotFoundError:
            # If the file doesn't exist, we just continue with an empty user dictionary
            self.users_role = {}
        except json.JSONDecodeError:
            # If there is an issue with decoding JSON data, handle the error
            print("Error: Invalid JSON data in the file.")
            self.users_role = {}  # Initialize to empty dictionary


    def save_users_role(self):
        # Transform the users_role dictionary into a list of dictionaries
        user_list = [{"user": username, **user_info} for username, user_info in self.users_role.items()]

        # Save the transformed user list to a JSON file
        with open(self.role_db, "w") as file:
            json.dump(user_list, file, indent=4)
            print("User roles saved to JSON file.")
############################################################
    def add_menu_item(self, item_name, price):
        # Load existing menu items
        self.load_menu_items()
        
        # Add or update the menu item
        self.menu[item_name] = price
        print(f"Added/Updated menu item: {item_name} - Price: {price}")
        
        # Save the updated menu items to the file
        self.save_menu_items()

    def save_menu_items(self):
        # Save the menu dictionary to a JSON file
        with open(self.menu_db, "w") as file:
            json.dump(self.menu, file, indent=4)
            print("Menu saved to JSON file.")

    def load_menu_items(self):
        # Load the menu items from the JSON file into the menu dictionary
        try:
            with open(self.menu_db, "r") as file:
                data = file.read()
                if data.strip():  # Check if the file is not empty
                    self.menu = json.loads(data)
                else:
                    self.menu = {}  # Initialize to empty dictionary if file is empty
        except FileNotFoundError:
            # If the file doesn't exist, create an empty JSON file
            with open(self.menu_db, "w") as file:
                file.write("{}")
            self.menu = {}  # Initialize to empty dictionary
        except json.JSONDecodeError:
            # If there is an issue with decoding JSON data, handle the error
            print("Error: Invalid JSON data in the file.")
            self.menu = {}  # Initialize to empty dictionary

    def view_all_menu_items(self):
        # Load existing menu items
        self.load_menu_items()

        if not self.menu:
            print("The menu is currently empty.")
            return

        print("All Menu Items:")
        for item_name, price in self.menu.items():
            print(f"{item_name}: {price}")
############################################################

    def add_table(self, table_number, capacity):
        # Add new table or update capacity if table exists
        self.tables[table_number] = capacity
        print(f"Added/Updated table: Table {table_number} - Capacity: {capacity}")

    def show_available_tables(self):
        # Show available tables
        if not self.tables:
            print("No tables are available at the moment.")
        else:
            print("Available Tables:")
            for table, capacity in self.tables.items():
                print(f"Table {table}: Capacity - {capacity}")

    def cancel_order(self, item_name):
        # Cancel order for specific food item
        if item_name in self.menu:
            del self.menu[item_name]
            print(f"Cancelled order for {item_name}.")
        else:
            print(f"Food item {item_name} is not available for order.")

# Example usage:

# Create users
manager = Manager("root", "root")
cashier = User("cashier1", "password456", "cashier")

# Authentication example:
username_input = input("Enter your username: ")
password_input = input("Enter your password: ")

if manager.authenticate(username_input, password_input):
    print("Authentication successful. Welcome, Manager!")
    print(manager)

    # Manager interface
    while True:
        print("\nManager Interface:")
        print("1. Add new user")
        print("2. View all users")
        print("3. Add/Update menu item")
        print("4. View all menu items")
        print("5. Add/Update table")
        print("6. Show available tables")
        print("7. Cancel order for specific food item")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            new_role = input("Enter new role: ")
            manager.add_user(new_username, new_password, new_role)
        elif choice == "2":
            manager.view_all_users()
        elif choice == "3":
            item_name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            manager.add_menu_item(item_name, price)
        elif choice == "4":
            manager.view_all_menu_items()
        elif choice == "5":
            table_number = input("Enter table number: ")
            capacity = int(input("Enter table capacity: "))
            manager.add_table(table_number, capacity)
        elif choice == "6":
            manager.show_available_tables()
        elif choice == "7":
            item_name = input("Enter item name to cancel order: ")
            manager.cancel_order(item_name)
        elif choice == "8":
            print("Exiting Manager Interface.")
            break
        else:
            print("Invalid choice. Please try again.")
elif cashier.authenticate(username_input, password_input):
    print("Authentication successful. Welcome, Cashier!")
    print(cashier)
else:
    print("Authentication failed. Please try again.")

