"""Representative post-generation test suite after Qodo Cover and bug-fix updates."""

import pytest

from app.calculator import (
    add,
    calculate_discount,
    divide,
    find_max_in_list,
    fizzbuzz,
    is_palindrome,
    multiply,
    subtract,
)


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2


def test_subtract_positive_numbers():
    assert subtract(10, 4) == 6


def test_multiply_by_zero():
    assert multiply(9, 0) == 0


def test_divide_regular_values():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_calculate_discount_regular_case():
    assert calculate_discount(100, 10) == 90


def test_calculate_discount_rejects_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_discount(-100, 10)


def test_calculate_discount_rejects_invalid_discount():
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        calculate_discount(100, 120)


def test_find_max_in_list_returns_highest_value():
    assert find_max_in_list([3, 9, 2, 5]) == 9


def test_find_max_in_list_rejects_empty_list():
    with pytest.raises(ValueError, match="List cannot be empty"):
        find_max_in_list([])


def test_is_palindrome_ignores_case_and_spaces():
    assert is_palindrome("Never Odd Or Even") is True


def test_fizzbuzz_multiple_of_three_and_five():
    assert fizzbuzz(15) == "FizzBuzz"


def test_fizzbuzz_regular_number():
    assert fizzbuzz(7) == "7"
