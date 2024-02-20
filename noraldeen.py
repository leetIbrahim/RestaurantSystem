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
        self.tables = {}  # Table number: Number of pax
        self.users = {}   # Username: User object

    def add_user(self, new_username, new_password, new_role):
        # Add new user to the system
        new_user = User(new_username, new_password, new_role)
        self.users[new_username] = new_user
        print(f"Added new user: {new_user}")

    def view_all_users(self):
        # View all users and their details
        print("All Users:")
        for username, user in self.users.items():
            print(user)

    def add_menu_item(self, item_name, price):
        # Add new item to the menu or update price if item exists
        self.menu[item_name] = price
        print(f"Added/Updated menu item: {item_name} - Price: {price}")

    def view_all_menu_items(self):
        # View all food items and their prices
        print("All Menu Items:")
        for item_name, price in self.menu.items():
            print(f"{item_name}: {price}")

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
manager = Manager("manager1", "password123")
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


#hello