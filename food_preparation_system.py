# food_preparation_system.py

def update_order_status(order_id, new_status):
    """Updates the status of a given order."""
    updated_lines = []
    found = False
    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == order_id:
                    parts[3] = new_status  # Update status at index 3
                    found = True
                updated_lines.append(','.join(parts))
        if found:
            with open('data/orders.txt', 'w') as file:
                file.writelines([f"{line}\n" for line in updated_lines])
            print(f"Order {order_id} status updated to '{new_status}'.")
        else:
            print(f"Order ID {order_id} not found.")
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")

def display_orders():
    """Displays all current orders with their statuses."""
    try:
        with open('data/orders.txt', 'r') as file:
            print("Current Orders and Their Statuses:")
            for line in file:
                parts = line.strip().split(',')
                if len(parts) > 3:  # Check for basic validity
                    print(f"Order ID: {parts[0]}, Status: {parts[3]}, Item: {parts[4]}, Quantity: {parts[5]}")
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")

def food_preparation_interface():
    while True:
        print("\n--- Food Preparation Interface ---")
        print("1. Display Orders")
        print("2. Update Order Status")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_orders()
        elif choice == '2':
            order_id = input("Enter the Order ID to update: ")
            print("Status Options: received, under_preparation, under_delivery, served")
            new_status = input("Enter the new status for the order: ")
            if new_status in ["received", "under_preparation", "under_delivery", "served"]:
                update_order_status(order_id, new_status)
            else:
                print("Invalid status entered.")
        elif choice == '3':
            print("Exiting Food Preparation Interface.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    food_preparation_interface()
