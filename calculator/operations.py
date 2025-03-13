"""
Operations Module.

This module provides basic arithmetic functions including addition, 
subtraction, multiplication, and division.
"""

from decimal import Decimal

def add_numbers(x: Decimal, y: Decimal) -> Decimal:
    """Returns the sum of two decimal numbers."""
    return x + y

def sub_numbers(x: Decimal, y: Decimal) -> Decimal:
    """Returns the difference between two decimal numbers."""
    return x - y

def mul_numbers(x: Decimal, y: Decimal) -> Decimal:
    """Returns the product of two decimal numbers."""
    return x * y

def div_numbers(x: Decimal, y: Decimal) -> Decimal:
    """Returns the quotient of two decimal numbers. Raises ValueError if divisor is zero."""
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y
