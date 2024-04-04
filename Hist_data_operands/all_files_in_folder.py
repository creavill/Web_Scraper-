class CoffeeShop:
    def __init__(self, name):
        self.name = name
        self.orders = {}

    def take_order(self, customer_name, coffee_type):
        self.orders[customer_name] = coffee_type
        print(f"{customer_name} ordered a {coffee_type}.")

    def fulfill_order(self, customer_name):
        coffee_type = self.orders.get(customer_name)
        if coffee_type:
            print(f"{customer_name}'s {coffee_type} is ready!")
            del self.orders[customer_name]
        else:
            print(f"Sorry, {customer_name} doesn't have an order.")

    def close_shop(self):
        print("Shop is now closed.")
        self.orders = {}


def main():
    coffee_shop = CoffeeShop("Starbucks")
    coffee_shop.take_order("Alice", "latte")
    coffee_shop.take_order("Bob", "espresso")
    coffee_shop.fulfill_order("Alice")
    coffee_shop.fulfill_order("Bob")
    coffee_shop.close_shop()

if __name__ == "__main__":
    main()

