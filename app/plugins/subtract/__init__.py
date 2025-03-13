"""
This module implements the subtraction command for a calculator application.
Handles decimal number subtraction with proper error checking and validation.
"""
from decimal import Decimal, InvalidOperation
from app.commands import Command
from calculator import CalcEngine

class SubtractCommand(Command): # pylint: disable=too-few-public-methods
    """Implements subtraction operation as a command pattern object.
    
    This class handles the execution of subtracting two decimal numbers,
    including input validation and error handling for invalid numeric inputs.
    """
    # pylint: disable=arguments-differ
    def execute(self, a_str: str, b_str: str) -> None:
        """Execute subtraction operation with two decimal number inputs.
        
        Args:
            a_str: String representation of the minuend (first number)
            b_str: String representation of the subtrahend (second number)
        """
        try:
            val_a = Decimal(a_str)
            val_b = Decimal(b_str)
        except InvalidOperation:
            print(f"Invalid number input: {a_str} or {b_str}  not a valid number.")
            return
        result = CalcEngine.difference(val_a, val_b)
        print(f"The result of {a_str} - {b_str} is {result}")
