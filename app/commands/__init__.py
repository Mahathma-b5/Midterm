"""Commands"""
from abc import ABC, abstractmethod

class Command(ABC): # pylint: disable=too-few-public-methods
    """Abstract Class"""
    @abstractmethod
    def execute(self):
        """Pass"""        
class CommandHandler:
    """Handler"""
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Registration of Commands"""
        self.commands[command_name] = command

    def execute_command(self, command_name: str):
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"No such command: {command_name}")
