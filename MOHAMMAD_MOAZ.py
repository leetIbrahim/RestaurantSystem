import time

#Display the order received and refresh the list. 

def display_orders():
    orders = []  #list to store orders
    print("Welcome to the Restaurant Order System!")
    print("Press 0 to quit.")
    print("Press 1 to refresh the order list.")
    print("Press 2 to add a new order.")
    print("Press 3 to delete an order.")
    print("Press 4 to update the status of an order.")
    print("Press 5 to block an order for a specific food item.")
    print()

    while True:
        action = int(input("Please enter an action (0-5): "))
        if action == 0:
            print("Exiting the order system.")
            break
        elif action == 1:
            print("Refreshing the order list...")
            print()
            display_orders()
        elif action == 2:
            order = input("Please enter the new order: ")
            orders.append({'order': order, 'status': 'under preparation'})
            print("Order added successfully.")
            print()
        elif action == 3:
            order_number = int(input("Please enter the order number you want to delete: "))
            if 1 <= order_number <= len(orders):
                del orders[order_number - 1]
                print(f"Order {order_number} deleted successfully.")
                print()
            else:
                print("Invalid order number. Please try again.")
                print()
        elif action == 4:
            order_number = int(input("Please enter the order number you want to update: "))
            if 1 <= order_number <= len(orders):
                order = orders[order_number - 1]
                status = input("Please enter the new status (under preparation/under delivery): ").lower()
                if status == 'under preparation' or status == 'under delivery':
                    order['status'] = status
                    print(f"Order {order_number} status updated successfully to {status}.")
                    print()
                else:
                    print("Invalid status. Please try again.")
                    print()
            else:
                print("Invalid order number. Please try again.")
                print()
        elif action == 5:
            food = input("Please enter the food item you want to block: ")
            blocked = True
            for order in orders:
                if food in order['order']:
                    order['status'] = 'blocked'
                if order['status'] != 'blocked':
                    blocked = False
            if blocked:
                print(f"All orders containing {food} have been blocked.")
            else:
                print(f"No orders containing {food} have been blocked.")
            print()
        else:
            print("Invalid action. Please try again.")
            print()

    #display the order list with numbers
    print("Order List:")
    for i, order in enumerate(orders, 1):
        if order['status'] == 'blocked':
            print(f"{i}. {order['order']} (blocked)")
        else:
            print(f"{i}. {order['order']} ({order['status']})")
    print()

def main():
    while True:
        display_orders()
        time.sleep(5)  #wait for 5 seconds before refreshing the list

if __name__ == "__main__":
    main()