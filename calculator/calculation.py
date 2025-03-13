"""Represents a Caluclation operations with two decimal operands."""
from decimal import Decimal
from typing import Callable

class OperationRecord:
    """Represents a mathematical operation with two decimal operands."""
    def __init__(self, x: Decimal, y: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """
        Initialize an operation record.

        :param x: First operand
        :param y: Second operand
        :param operation: A function that performs the operation
        """
        self.x = x
        self.y = y
        self.operation = operation

    def execute(self) -> Decimal:
        """
        Execute the stored operation.

        :return: The result of applying the operation to x and y
        """
        return self.operation(self.x, self.y)

    @staticmethod
    def create(
        x: Decimal, y: Decimal, operation: Callable[[Decimal, Decimal], Decimal]
        ) -> 'OperationRecord':
        """
        Factory method to create an OperationRecord instance.

        :param x: First operand
        :param y: Second operand
        :param operation: A function that performs the operation
        :return: A new OperationRecord instance
        """
        return OperationRecord(x, y, operation)

    def __repr__(self) -> str:
        """
        String representation of the operation record.

        :return: A formatted string representation
        """
        return f"OperationRecord({self.x}, {self.y}, {self.operation.__name__})"
    @property
    def symbol(self) -> str:
        """
        Get the mathematical symbol corresponding to the operation function.

        :return: A string representing the operation symbol
        """
        operation_map = {
            'add_numbers': '+',
            'sub_numbers': '-',
            'mul_numbers': '×',
            'div_numbers': '÷'
        }
        return operation_map.get(self.operation.__name__, '?')
