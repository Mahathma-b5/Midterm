"""Plugin For Menu"""
from app.commands import Command # type: ignore


class MenuCommand(Command): # pylint: disable=too-few-public-methods
    """Menu Command"""
    def __init__(self, command_handler):
        self.command_handler = command_handler
    def execute(self):
        available_commands = list(self.command_handler.commands.keys())
        print("Available commands:")
        for command in available_commands:
            print(f"- {command}")
