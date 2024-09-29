from datetime import datetime
import hashlib
import chef_services

def display_orders():
    """Display all received orders."""
    print("ready-made orders:")
    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                order_id, table_id, waiter_id, status, details = line.strip().split(',', 4)
                if status == "under_delivery":
                    print(f"Order ID: {order_id}, Table ID: {table_id}, Details: {details}")
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")


def generate_next_order_id():
    """Generates the next order ID based on the highest current ID."""
    try:
        with open('data/orders.txt', 'r') as file:
            order_ids = [int(line.split(',')[0]) for line in file if line.strip() and line.split(',')[0].isdigit()]
        next_order_id = max(order_ids) + 1 if order_ids else 1
    except FileNotFoundError:
        next_order_id = 1
    return next_order_id



def show_available_tables():
    print("Available Tables:")
    try:
        with open('data/tables.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                table_id, pax, status = parts[0], parts[1], parts[2]
                if status == "free":
                    print(f"Table ID: {table_id}, Pax: {pax}")
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")



def check_in_customer():
    show_available_tables()
    table_id = input("Enter the table ID to check in customer: ")
    customer_pax = int(input("Enter number of pax: "))
    waiter_id = input("Enter your Waiter/Waitress ID: ")
    updated = False
    tables = []

    try:
        with open('data/tables.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                id, pax, status = parts[0], parts[1], parts[2]
                if id == table_id:
                    if status == "free" and int(pax) >= customer_pax:
                        tables.append(f"{id},{pax},occupied,{waiter_id}\n")
                        updated = True
                    else:
                        tables.append(line)
                else:
                    tables.append(line)
        
        if updated:
            with open('data/tables.txt', 'w') as file:
                file.writelines(tables)
            print(f"Customer checked in at Table {table_id}.")
            # After successfully checking in, prompt to take orders for the table
            take_order(table_id, customer_pax, waiter_id)
        else:
            print("Unable to check in customer. Please ensure the table is available and can accommodate the pax.")

    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")



def read_menu_items():
    menu_items = []
    try:
        with open('data/menu.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                # Assuming the second element is the item name
                item_name = parts[1]
                menu_items.append(item_name)
    except FileNotFoundError:
        print("Menu file not found. Please ensure the 'data/menu.txt' file exists.")
    return menu_items


def read_menu_items_with_prices():
    menu_items = {}
    try:
        with open('data/menu.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 4 and parts[3] == 'blocked':
                    continue  # Skip blocked items
                item_name, item_price = parts[1], parts[2]
                menu_items[item_name] = item_price
    except FileNotFoundError:
        print("Menu file not found. Please ensure the 'data/menu.txt' file exists.")
    return menu_items



def take_order(table_id, customer_pax, waiter_id):
    print(f"Taking orders for {customer_pax} customers at Table {table_id} served by Waiter/Waitress ID {waiter_id}.")
    menu_items_with_prices = read_menu_items_with_prices()  # Fetch the menu excluding blocked items

    orders = []
    for i in range(customer_pax):
        print("Available menu items:")
        for item, price in menu_items_with_prices.items():
            print(f"{item}: {price}")
        
        while True:
            item_name = input(f"Enter order for customer {i+1}: ")
            if item_name in menu_items_with_prices:
                quantity = input(f"Enter quantity for {item_name}: ")
                try:
                    quantity = int(quantity)
                    item_price = float(menu_items_with_prices[item_name]) * quantity
                    order_id = generate_next_order_id()  # Generate unique order ID for each order
                    # Assuming each order line includes order_id, table_id, waiter_id, status, item_name, quantity, and the total price
                    order_line = f"{order_id},{table_id},{waiter_id},received,{item_name},{quantity},{item_price:.2f}\n"
                    orders.append(order_line)
                    print(f"Added {quantity} of {item_name} to the order at total price {item_price:.2f}.")
                    break  # Break the loop and proceed to the next customer/order
                except ValueError:
                    print("Invalid quantity. Please enter a numeric value.")
            else:
                print("This item is not available. Please choose an available item from the menu.")

    # After collecting all orders, write them to the orders.txt file
    try:
        with open('data/orders.txt', 'a') as file:
            for order in orders:
                file.write(order)
        print("Orders successfully taken and recorded.")
        chef_services.chef_interface()
    except Exception as e:
        print(f"Error recording orders: {e}")




def update_order_status_to_received():
    order_id = input("Enter the order ID to mark as received: ")
    update_order_status(order_id, "order_received")

def update_order_status(order_id, new_status):
    updated = False
    orders = []

    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                id, table_id, waiter_id, _, details = line.strip().split(',', 4)  # Updated to ignore previous status
                if id == order_id:
                    orders.append(f"{id},{table_id},{waiter_id},{new_status},{details}\n")
                    updated = True
                else:
                    orders.append(line)
        
        if updated:
            with open('data/orders.txt', 'w') as file:
                file.writelines(orders)
            print(f"Order {order_id} updated to {new_status}.")
        else:
            print("Order ID not found.")
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")


def update_order_status_to_served():
    order_id = input("Enter the order ID to mark as served: ")
    update_order_status(order_id, "served")


def check_out_customer():
    table_id = input("Enter the table ID to check out: ")
    update_table_status(table_id, "needs_cleaning")
    print(f"Table {table_id} marked for cleaning.")

def clean_table():
    table_id = input("Enter the table ID to mark as clean: ")
    update_table_status(table_id, "free")
    print(f"Table {table_id} is now free and clean.")

def update_table_status(table_id, new_status):
    updated = False
    tables = []

    try:
        with open('data/tables.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                id, pax, status = parts[0], parts[1], parts[-1]  # Last part is always status
                if id == table_id:
                    if new_status == "free":  # Reset to 'free' without waiter ID
                        tables.append(f"{id},{pax},{new_status}\n")
                    else:  # Preserve waiter ID for other statuses if needed
                        tables.append(f"{','.join(parts[:-1])},{new_status}\n")
                    updated = True
                else:
                    tables.append(line)
        
        if updated:
            with open('data/tables.txt', 'w') as file:
                file.writelines(tables)
            print(f"Table {table_id} status updated to {new_status}.")
        else:
            print("Table ID not found.")
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")

def is_table_free(table_id):
    """Checks if the specified table is free."""
    try:
        with open('data/tables.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == table_id:
                    return parts[2] == 'free'
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")
        return False  # Assume not free if file not found
    return False  # Assume not free if table ID not found

def accept_reservation():
    while True:  # Keep asking until a free table is selected
        table_id = input("Enter table ID for the reservation: ")
        if is_table_free(table_id):
            break  # Exit the loop if the table is free
        else:
            print("This table is not available. Please choose another table.")
            continue

    # Proceed with the rest of the reservation process
    customer_name = input("Enter customer name: ")
    contact_number = input("Enter contact number: ")
    number_of_pax = input("Enter number of pax: ")
    reservation_date_time = input("Enter reservation date and time (YYYY-MM-DD HH:MM): ")
    
    # Generate reservation code
    reservation_code = generate_reservation_code(customer_name, contact_number, table_id, reservation_date_time)
    
    # Save reservation details
    with open('data/reservations.txt', 'a') as file:
        file.write(f"{reservation_code},{customer_name},{contact_number},{number_of_pax},{table_id},{reservation_date_time}\n")
    print(f"Reservation made successfully. Reservation Code: {reservation_code}")
    
    # Block the table for this reservation
    block_table_for_reservation(table_id, reservation_date_time)  # Update the table's status to 'reserved' or similar


def accept_reservation():
    customer_name = input("Enter customer name: ")
    contact_number = input("Enter contact number: ")
    number_of_pax = input("Enter number of pax: ")
    table_id = input("Enter table ID for the reservation: ")
    reservation_date_time = input("Enter reservation date and time (YYYY-MM-DD HH:MM): ")
    
    # Check if the table is free before proceeding with the reservation
    if is_table_free(table_id):
        # Proceed with reservation since the table is free
        reservation_code = generate_reservation_code(customer_name, contact_number, table_id, reservation_date_time)
        with open('data/reservations.txt', 'a') as file:
            file.write(f"{reservation_code},{customer_name},{contact_number},{number_of_pax},{table_id},{reservation_date_time}\n")
        print(f"Reservation made successfully. Reservation Code: {reservation_code}")
        
        # Optionally, update the table's status to 'reserved' in tables.txt
        block_table_for_reservation(table_id, reservation_date_time)
    else:
        # Inform the user the table is not available for reservation
        print("The selected table is not available for reservation. Please choose another table or try a different time.")


def generate_reservation_code(customer_name, contact_number, table_id, reservation_date_time):
    # Create a base string from the reservation details
    base_str = f"{customer_name}{contact_number}{table_id}{reservation_date_time}"
    
    # Use hashlib to generate a hex digest for uniqueness
    hash_object = hashlib.md5(base_str.encode())
    reservation_code = hash_object.hexdigest()[:6]  # Take first 6 characters for brevity
    
    return reservation_code

# Example usage within accept_reservation
def accept_reservation():
    while True:  # Keep asking for a table ID until a free table is found or the user decides to stop trying.
        table_id = input("Enter table ID for the reservation: ")
        if is_table_free(table_id):
            break  # Exit the loop if the table is free.
        else:
            print("Table is not free or not found. Please try a different table ID.")
            continue_choice = input("Try another table? (yes/no): ").lower()
            if continue_choice != 'yes':
                print("Reservation cancelled.")
                return  # Exit the function if the user decides not to continue.

    # Proceed with the reservation since the table is free.
    customer_name = input("Enter customer name: ")
    contact_number = input("Enter contact number: ")
    number_of_pax = input("Enter number of pax: ")
    reservation_date_time = input("Enter reservation date and time (YYYY-MM-DD HH:MM): ")

    # Generate reservation code using the generate_reservation_code function.
    reservation_code = generate_reservation_code(customer_name, contact_number, table_id, reservation_date_time)

    # Save reservation details to file.
    with open('data/reservations.txt', 'a') as file:
        file.write(f"{reservation_code},{customer_name},{contact_number},{number_of_pax},{table_id},{reservation_date_time}\n")
    print(f"Reservation made successfully. Reservation Code: {reservation_code}")
    
    # Optionally, you can add a call to block the table for reservation here.
    # Remember to update the table's status in `tables.txt` from 'free' to 'reserved'.



def retrieve_reservation_by_code():
    reservation_code = input("Enter the reservation code: ")
    found = False
    try:
        with open('data/reservations.txt', 'r') as file:
            for line in file:
                # Assuming the reservation code is the first element in each line
                code, customer_name, contact_number, number_of_pax, table_id, reservation_date_time = line.strip().split(',', 5)
                if code == reservation_code:
                    print(f"Reservation Found:\n- Customer Name: {customer_name}\n- Contact Number: {contact_number}\n- Number of Pax: {number_of_pax}\n- Table ID: {table_id}\n- Reservation Date and Time: {reservation_date_time}")
                    found = True
                    break  # Exit the loop since we found the reservation
    except FileNotFoundError:
        print("Reservations file not found. Please ensure the 'data/reservations.txt' file exists.")
    
    if not found:
        print("No reservation found for the provided code.")

def block_table_for_reservation(table_id, reservation_date_time):
    updated = False
    tables = []

    try:
        with open('data/tables.txt', 'r') as file:
            for line in file:
                id, pax, status = line.strip().split(',')
                if id == table_id:
                    # This simplistic approach does not account for the timing aspect in a real-time manner.
                    # It assumes an external process for managing reservation times.
                    tables.append(f"{id},{pax},reserved\n")
                    updated = True
                else:
                    tables.append(line)
        
        if updated:
            with open('data/tables.txt', 'w') as file:
                file.writelines(tables)
            print(f"Table {table_id} reserved for {reservation_date_time}.")
        else:
            print("Table ID not found.")
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")


def update_table_status(table_id, new_status, employee_name=None):
    """Helper function to update the status of a given table. Appends employee name if status is 'occupied'."""
    updated_lines = []
    found = False
    try:
        with open('data/tables.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == table_id:
                    if new_status == "free":
                        parts = [parts[0], parts[1], new_status]  # Reset to just table_id, pax, and status
                    else:
                        parts[2] = new_status  # Update status
                        if employee_name and new_status == "occupied":
                            # Append employee name only if updating to 'occupied'
                            parts.append(employee_name)
                    found = True
                updated_lines.append(','.join(parts))
        if found:
            with open('data/tables.txt', 'w') as file:
                file.writelines([f"{line}\n" for line in updated_lines])
            status_msg = "free, ready for new customers" if new_status == "free" else f"occupied by {employee_name}"
            print(f"Table {table_id} status updated to '{status_msg}'.")
        else:
            print(f"Table {table_id} not found.")
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")


def waiter_interface():
    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║   Waiter/Waitress Interface            ║")
        print("╠════════════════════════════════════════╣")
        print("║ 1. Show Available Tables               ║")
        print("║ 2. Show Ready-made Orders              ║")
        print("║ 3. Check-In Customer                   ║")
        print("║ 4. Take Order                          ║")
        print("║ 5. Mark Order as Received              ║")
        print("║ 6. Mark Order as Served                ║")
        print("║ 7. Check-Out Customer                  ║")
        print("║ 8. Clean Table                         ║")
        print("║ 9. Accept Reservation                  ║")
        print("║ 10. Show Reservations                  ║")
        print("║ 11. Exit                               ║")
        print("╚════════════════════════════════════════╝")
        choice = input("\nEnter your choice (1-10): ")


        if choice == '1':
            show_available_tables()
        elif choice == '2':
            display_orders()
        elif choice == '3':
            check_in_customer()
        elif choice == '4':
            # This assumes you have a way to determine or input these details
            table_id = input("Enter the table ID for taking orders: ")
            # You might want to fetch customer_pax based on the table_id from tables.txt
            customer_pax = int(input("Enter number of pax at the table: "))
            waiter_id = input("Enter your Waiter/Waitress ID: ")
            take_order(table_id, customer_pax, waiter_id)
        elif choice == '5':
            update_order_status_to_received()
        elif choice == '6':
            update_order_status_to_served()
        elif choice == '7':
            check_out_customer()
        elif choice == '8':
            clean_table()
        elif choice == '9':
            accept_reservation()
        elif choice == '10':
            retrieve_reservation_by_code()
        elif choice == '11':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    waiter_interface()
