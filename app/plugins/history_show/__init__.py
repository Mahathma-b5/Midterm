"""Shows History"""
from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class HistoryShowCommand(Command): # pylint: disable=too-few-public-methods
    """Command For Showing History"""
    def execute(self):
        entries = HistoryFacade.get_formatted_history()
        if not entries:
            print("No history available")
            return
        print("\nOperation History:")
        for idx, entry in enumerate(entries, 1):
            print(f"{idx}. {entry}")
