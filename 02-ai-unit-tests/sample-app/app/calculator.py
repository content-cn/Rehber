"""A simple calculator module with deliberately low test coverage and a subtle bug."""


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Return the division of a by b. Raises ValueError for division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate_discount(price, discount_percent):
    """Return the final price after applying a discount percentage (0-100).
    Should reject negative prices and discounts outside 0-100 range."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    # BUG: Does not validate negative prices (docstring says it should)
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


def find_max_in_list(numbers):
    """Return the maximum value in a non-empty list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    max_val = numbers[0]
    for i in range(1, len(numbers)):
        # BUG: Uses < instead of > — this actually finds the MINIMUM
        if numbers[i] < max_val:
            max_val = numbers[i]
    return max_val


def is_palindrome(text):
    """Check if text is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def fizzbuzz(n):
    """Return 'FizzBuzz' for multiples of both 3 and 5, 'Fizz' for multiples of 3,
    'Buzz' for multiples of 5, or the number as a string."""
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return str(n)
