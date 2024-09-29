def display_orders():
    print("Received Orders:")
    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                # Check if the line format starts with a numeric order_id
                if len(parts) == 7 and parts[0].isdigit():
                    order_id, table_id, waiter_id, status, item_name, quantity, price = parts
                    print(f"Order ID: {order_id}, Table ID: {table_id}, Waiter ID: {waiter_id}, Status: {status}, Item: {item_name}, Quantity: {quantity}, Price: {price}")
                else:
                    print(f"Line in unexpected format or missing order ID: {line.strip()}")
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")



def update_order_status():
    order_id_to_update = input("Enter the order ID to update: ")
    new_status = input("Enter new status ('under_preparation' or 'under_delivery'): ")
    updated = False
    updated_orders = []

    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == order_id_to_update:
                    # Assuming the status is always the fourth component
                    parts[3] = new_status  # Update the status
                    updated_line = ','.join(parts) + '\n'
                    updated_orders.append(updated_line)
                    updated = True
                else:
                    updated_orders.append(line)
                    
        if updated:
            with open('data/orders.txt', 'w') as file:
                file.writelines(updated_orders)
            print(f"Order {order_id_to_update} updated to {new_status}.")
        else:
            print(f"Order ID {order_id_to_update} not found.")
            
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")


def cancel_order():
    order_id = input("Enter the order ID to cancel/block: ")
    reason = input("Enter reason for cancellation/blocking: ")
    updated = False
    orders = []
    
    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) < 6:
                    print(f"Skipping line due to unexpected format: {line.strip()}")
                    continue  # Skip lines that do not conform to the expected format
                id, table_id, waiter_id, status, item, price = parts
                if id == order_id:
                    orders.append(f"{id},{table_id},{waiter_id},cancelled_due_to_{reason},{item},{price}\n")
                    updated = True
                else:
                    orders.append(line)
        
        if updated:
            with open('data/orders.txt', 'w') as file:
                file.writelines(orders)
            print(f"Order {order_id} cancelled due to {reason}.")
        else:
            print("Order ID not found.")
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")


def chef_interface():
    while True:
        print("\n╔════════════════════════════════════╗")
        print("║         Chef Interface             ║")
        print("╠════════════════════════════════════╣")
        print("║ 1. Display Orders                  ║")
        print("║ 2. Update Order Status             ║")
        print("║ 3. Cancel Order                    ║")
        print("║ 4. Exit                            ║")
        print("╚════════════════════════════════════╝")
        
        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            display_orders()
        elif choice == '2':
            update_order_status()
        elif choice == '3':
            cancel_order()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    chef_interface()
