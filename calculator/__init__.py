"""
This module provides calculation engine functionality for basic arithmetic operations,
including history tracking of all performed operations.
"""
from decimal import Decimal
from typing import Callable
from calculator.operations import add_numbers, sub_numbers, mul_numbers, div_numbers
from calculator.calculation import OperationRecord
from calculator.history.history import OperationHistory # type: ignore


class CalcEngine:
    """Engine class for performing calculations and maintaining operation history.
    
    Provides static methods for basic arithmetic operations while automatically
    recording each operation in the calculation history.
    """
    @staticmethod
    def _execute_operation(
        x: Decimal,
        y: Decimal, op_func: Callable[[Decimal, Decimal], Decimal]
        ) -> Decimal:
        """Execute a calculation operation and store it in history.
        
        Args:
            x: First operand
            y: Second operand
            op_func: Operation function to execute
            
        Returns:
            Decimal: Result of the operation
        """
        record = OperationRecord.create(x, y, op_func)
        OperationHistory.add_record(record)
        return record.execute()

    @staticmethod
    def sum_values(x: Decimal, y: Decimal) -> Decimal:
        """Calculate the sum of two decimal values.
        
        Args:
            x: First addend
            y: Second addend
            
        Returns:
            Decimal: Sum of x and y
        """
        return CalcEngine._execute_operation(x, y, add_numbers)

    @staticmethod
    def difference(x: Decimal, y: Decimal) -> Decimal:
        """Calculate the difference between two decimal values.
        
        Args:
            x: Minuend
            y: Subtrahend
            
        Returns:
            Decimal: Result of x - y
        """
        return CalcEngine._execute_operation(x, y, sub_numbers)

    @staticmethod
    def product(x: Decimal, y: Decimal) -> Decimal:
        """Calculate the product of two decimal values.
        
        Args:
            x: Multiplicand
            y: Multiplier
            
        Returns:
            Decimal: Result of x * y
        """
        return CalcEngine._execute_operation(x, y, mul_numbers)

    @staticmethod
    def quotient(x: Decimal, y: Decimal) -> Decimal:
        """Calculate the quotient of two decimal values.
        
        Args:
            x: Dividend
            y: Divisor
            
        Returns:
            Decimal: Result of x / y
            
        Raises:
            DivisionByZero: If divisor is zero
        """
        return CalcEngine._execute_operation(x, y, div_numbers)
