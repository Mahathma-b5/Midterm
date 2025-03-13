"""
Command module for handling application exit functionality.
Provides clean termination capability through command pattern implementation.
"""
import sys
from app.commands import Command


class ExitCommand(Command):# pylint: disable=too-few-public-methods
    """Command implementation for gracefully exiting the application.
    
    Implements the Command pattern interface to provide consistent
    termination behavior across different execution contexts.
    """
    def execute(self):
        """Trigger application shutdown with exit message."""
        sys.exit("Exiting...")
