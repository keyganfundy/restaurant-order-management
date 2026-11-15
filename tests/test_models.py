import unittest

from models import Customer, MenuItem, Order, Restaurant


class TestModels(unittest.TestCase):

    def test_customer_creation(self):
        customer = Customer(1, "John Smith", "555-1234")
        self.assertEqual(customer.name, "John Smith")

    def test_menu_item_creation(self):
        item = MenuItem(1, "Burger", 8.99)
        self.assertEqual(item.price, 8.99)

    def test_order_total(self):
        customer = Customer(1, "John Smith")
        order = Order(1001, customer)
        order.add_item(MenuItem(1, "Burger", 8.99))
        order.add_item(MenuItem(2, "Fries", 3.49))

        self.assertAlmostEqual(order.total(), 12.48)

    def test_invalid_customer(self):
        with self.assertRaises(ValueError):
            Customer(1, "")

    def test_invalid_menu_price(self):
        with self.assertRaises(ValueError):
            MenuItem(1, "Burger", -1.00)

    def test_restaurant_rejects_duplicate_customer(self):
        restaurant = Restaurant("Test Restaurant")
        restaurant.add_customer(Customer(1, "John"))

        with self.assertRaises(ValueError):
            restaurant.add_customer(Customer(1, "Jane"))


if __name__ == "__main__":
    unittest.main()
