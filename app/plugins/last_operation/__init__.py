"""Picks and shows final operation"""
from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class LastOpCommand(Command): # pylint: disable=too-few-public-methods
    """"Command for final operation"""
    def execute(self):
        formatted_op = HistoryFacade.get_last_formatted()
        print(f"final operation: {formatted_op}")
