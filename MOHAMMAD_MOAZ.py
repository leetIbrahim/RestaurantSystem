orders = []
#Display the order received and refresh the list. 

def display_orders():
    """Display the current list of orders."""
    print("Current orders:")
    for i, order in enumerate(orders, 1):
        print(f"{i}. {order}")

def add_order():
    """Add a new order to the list."""
    order = input("Enter the order: ")
    orders.append(order)
    print(f"Order '{order}' added to the list.")
    display_orders()

def refresh_orders():
    """Clear and re-display the list of orders."""
    global orders
    orders = []
    print("Orders list refreshed.")
    display_orders()

def main():
    while True:
        print("\n1. Display orders")
        print("2. Add order")
        print("3. Refresh orders")
        print("4. Quit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            display_orders()
        elif choice == 2:
            add_order()
        elif choice == 3:
            refresh_orders()
        elif choice == 4:
            print("Quitting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()