"""
History loading command module for calculator application.
Provides interactive CSV history file selection and loading capabilities.
"""
from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class HistoryLoadCommand(Command):# pylint: disable=too-few-public-methods
    """Implements interactive history loading through command pattern.
    
    Handles CSV file discovery, user selection, and error handling for
    historical data loading operations.
    """
    def execute(self):
        """Execute interactive history loading workflow."""
        try:
            # List available CSV files
            csv_files = HistoryFacade.list_csv_files()
            if not csv_files:
                print("No history files found in current directory.")
                return

            # Display file selection menu
            print("\nAvailable history files:")
            for idx, file in enumerate(csv_files, 1):
                print(f"{idx}. {file.name}")

            # Get user selection
            while True:
                try:
                    selection = int(input("\nEnter file number to load (0 to cancel): "))
                    if selection == 0:
                        return
                    if 1 <= selection <= len(csv_files):
                        selected_file = csv_files[selection-1].name
                        break
                    print("Invalid selection. Please enter a valid number.")
                except ValueError:
                    print("Please enter a numeric value.")

            # Load and display history
            result = HistoryFacade.load_from_csv(selected_file)
            print(f"\n{result}")

        except (FileNotFoundError, PermissionError, ValueError) as e:
            print(f"File operation failed: {str(e)}")
