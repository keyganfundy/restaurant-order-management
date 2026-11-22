"""Input validation helpers shared by the GUI and unit tests."""
def required_text(value, field_name):
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be blank.")
    return cleaned

def positive_integer(value, field_name):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a whole number.") from None
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")
    return number

def nonnegative_price(value):
    try:
        price = float(value)
    except (TypeError, ValueError):
        raise ValueError("Price must be a number, such as 8.99.") from None
    if price < 0:
        raise ValueError("Price cannot be negative.")
    return round(price, 2)
