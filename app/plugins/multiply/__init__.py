"""
Multiplication command implementation for calculator application.
Handles decimal multiplication with input validation and error handling.
"""
from decimal import Decimal, InvalidOperation
from app.commands import Command
from calculator import CalcEngine

class MultiplyCommand(Command):    # pylint: disable=too-few-public-methods
    """Implements multiplication operation following command pattern.
    
    Responsible for validating decimal inputs and executing multiplication
    through CalcEngine while maintaining Liskov Substitution Principle.
    """
    # pylint: disable=arguments-differ
    def execute(self, a_str: str, b_str: str) -> None:
        """Execute multiplication with validated decimal inputs.
        
        Args:
            a_str: Multiplicand as string
            b_str: Multiplier as string
        """
        try:
            val_a = Decimal(a_str)
            val_b = Decimal(b_str)
        except InvalidOperation:
            print(f"Invalid number input: {a_str} or {b_str} is not valid number.")
            return
        # Calculate the product
        result = CalcEngine.product(val_a, val_b)
        if result == 0:
            result = 0
        print(f"The result of {a_str} * {b_str} is {result}")
