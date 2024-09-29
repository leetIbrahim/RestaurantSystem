# table_management_system.py

def update_table_status(table_id, new_status):
    """Helper function to update the status of a given table and clear waiter ID if table is set to free."""
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
                        parts[2] = new_status  # Update status while keeping existing waiter_id
                    found = True
                updated_lines.append(','.join(parts))
        if found:
            with open('data/tables.txt', 'w') as file:
                file.writelines([f"{line}\n" for line in updated_lines])
            status_msg = "free, ready for new customers" if new_status == "free" else new_status
            print(f"Table {table_id} status updated to '{status_msg}'.")
        else:
            print(f"Table {table_id} not found.")
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")

def reserve_table():
    table_id = input("Enter Table ID to reserve: ")
    waiter_id = input("Enter Waiter/Waitress ID for the reservation: ")
    update_table_status(table_id, 'occupied', waiter_id)
    print(f"Table {table_id} reserved (occupied) under Waiter/Waitress ID: {waiter_id}.")

def check_in_table():
    table_id = input("Enter Table ID for check-in: ")
    waiter_id = input("Enter Waiter/Waitress ID: ")
    update_table_status(table_id, 'occupied', waiter_id)
    print(f"Table {table_id} checked in (occupied), served by Waiter/Waitress ID: {waiter_id}.")

def check_out_table():
    table_id = input("Enter Table ID for check-out: ")
    # Waiter ID might not be needed for check-out, but if cleanup assignments are tracked, it could be added here.
    update_table_status(table_id, 'needs_cleaning')
    print(f"Table {table_id} checked out, awaiting cleaning.")

def clean_table():
    table_id = input("Enter Table ID to clean: ")
    update_table_status(table_id, 'free')
    print(f"Table {table_id} is now clean and free.")


def show_table_status():
    """Displays the status of all tables with standardized status terminology."""
    try:
        with open('data/tables.txt', 'r') as file:
            print("Current Table Statuses:")
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    table_id, pax, status = parts[:3]
                    print(f"Table ID: {table_id}, Pax: {pax}, Status: {status}")
                else:
                    print(f"Skipped line due to unexpected format: {line.strip()}")
    except FileNotFoundError:
        print("Tables file not found. Please ensure the 'data/tables.txt' file exists.")

def table_management_interface():
    while True:
        print("\n--- Table Management Interface ---")
        print("1. Show Table Status")
        print("2. Reserve a Table")
        print("3. Check-in a Table")
        print("4. Check-out a Table")
        print("5. Clean a Table")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            show_table_status()
        elif choice == '2':
            reserve_table()
        elif choice == '3':
            check_in_table()
        elif choice == '4':
            check_out_table()
        elif choice == '5':
            clean_table()
        elif choice == '6':
            print("Exiting Table Management Interface.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    table_management_interface()
