"""Command module for addition operation in calculator application."""
from decimal import Decimal, InvalidOperation
from app.commands import Command
from calculator import CalcEngine

class AddCommand(Command): # pylint: disable=too-few-public-methods
        # pylint: disable=arguments-differ
    """A command class for performing addition operations."""    
    def execute(self, a_str: str, b_str: str) -> None:
        """Execute addition command with two numeric arguments.
        
        Args:
            args: Variable length argument list expecting two string numbers
        """
        try:
            val_a = Decimal(a_str)
            val_b = Decimal(b_str)
        except InvalidOperation:
            print(f"Invalid number input: {a_str} or {b_str} is not a valid number.")
            return
        result = CalcEngine.sum_values(val_a, val_b)
        print(f"The result of {a_str} + {b_str} is {result}")
