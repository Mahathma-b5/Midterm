"""Plugin for History Saving to CSV"""
from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class HistorySaveCommand(Command): # pylint: disable=too-few-public-methods
    """Class for History Saving to CSV Command"""
    def execute(self):
        result = HistoryFacade.save_to_csv()
        print(result)
