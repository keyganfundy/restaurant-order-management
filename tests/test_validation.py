import unittest
from validation import required_text, positive_integer, nonnegative_price

class TestValidation(unittest.TestCase):
    def test_required_text_trims_spaces(self):
        self.assertEqual(required_text("  Burger  ", "Name"), "Burger")

    def test_required_text_rejects_blank(self):
        with self.assertRaises(ValueError):
            required_text("   ", "Name")

    def test_positive_integer(self):
        self.assertEqual(positive_integer("12", "ID"), 12)

    def test_invalid_integer_rejected(self):
        with self.assertRaises(ValueError):
            positive_integer("abc", "ID")

    def test_nonnegative_price(self):
        self.assertEqual(nonnegative_price("8.99"), 8.99)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            nonnegative_price("-2.00")

if __name__ == "__main__":
    unittest.main()
