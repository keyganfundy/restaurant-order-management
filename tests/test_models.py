import unittest
from models import Customer, MenuItem, Order, Restaurant

class TestModels(unittest.TestCase):
    def test_customer_creation(self):
        self.assertEqual(Customer(1, "Jordan").name, "Jordan")

    def test_menu_item_creation(self):
        self.assertEqual(MenuItem(1, "Burger", 8.99).price, 8.99)

    def test_order_total(self):
        customer = Customer(1, "Jordan")
        order = Order(1, customer, [MenuItem(1, "Burger", 8.99), MenuItem(2, "Fries", 3.49)])
        self.assertAlmostEqual(order.total(), 12.48)

    def test_blank_customer_rejected(self):
        with self.assertRaises(ValueError):
            Customer(1, " ")

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            MenuItem(1, "Burger", -1)

    def test_duplicate_customer_rejected(self):
        restaurant = Restaurant("Test")
        restaurant.add_customer(Customer(1, "Jordan"))
        with self.assertRaises(ValueError):
            restaurant.add_customer(Customer(1, "Taylor"))

if __name__ == "__main__":
    unittest.main()
