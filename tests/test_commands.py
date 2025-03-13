"""Tests For Basic Commands"""
import pytest
from app import App
from app.plugins.add import AddCommand
from app.plugins.subtract import SubtractCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.divide import DivideCommand
from app.commands import Command

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit) as exit_info:
        app = App(start_repl=False)  # Prevent auto-start of REPL
        app.run_repl()

    # Check that the expected output was printed
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out
    assert str(exit_info.value) == "Exiting..."

def test_add_command_valid_input(monkeypatch, capfd):
    """Test AddCommand with valid input."""
    # Simulate user input for valid numbers
    monkeypatch.setattr(
        'builtins.input', lambda _: '10 20')  # Example: '10' and '20' are the inputs

    add_command = AddCommand()
    add_command.execute('10', '20')  # Simulate adding 10 and 20

    captured = capfd.readouterr()
    assert "The result of 10 + 20 is 30" in captured.out

def test_add_command_invalid_input(monkeypatch, capfd):
    """Test AddCommand with invalid input (non-numeric values)."""
    # Simulate user input with invalid numbers
    monkeypatch.setattr('builtins.input', lambda _: '10 abc')  # 'abc' is invalid

    add_command = AddCommand()
    add_command.execute('10', 'abc')  # Simulate adding 10 and 'abc'

    captured = capfd.readouterr()
    assert "Invalid number input: 10 or abc is not a valid number." in captured.out

def test_add_command_edge_case(monkeypatch, capfd):
    """Test AddCommand with edge cases like zero or negative numbers."""
    monkeypatch.setattr('builtins.input', lambda _: '0 -5')  # Example: '0' and '-5'

    add_command = AddCommand()
    add_command.execute('0', '-5')  # Simulate adding 0 and -5

    captured = capfd.readouterr()
    assert "The result of 0 + -5 is -5" in captured.out

def test_subtract_command_valid_input(monkeypatch, capfd):
    """Test SubtractCommand with valid input."""
    # Simulate user input for valid numbers
    monkeypatch.setattr('builtins.input', lambda _: '15 5')  # Example: '15' and '5' are the inputs

    subtract_command = SubtractCommand()
    subtract_command.execute('15', '5')  # Simulate subtracting 15 and 5

    captured = capfd.readouterr()
    assert "The result of 15 - 5 is 10" in captured.out

def test_subtract_command_invalid_input(monkeypatch, capfd):
    """Test SubtractCommand with invalid input (non-numeric values)."""
    # Simulate user input with invalid numbers
    monkeypatch.setattr('builtins.input', lambda _: '10 abc')  # 'abc' is invalid

    subtract_command = SubtractCommand()
    subtract_command.execute('10', 'abc')  # Simulate subtracting 10 and 'abc'

    captured = capfd.readouterr()
    assert "Invalid number input: 10 or abc  not a valid number." in captured.out

def test_subtract_command_edge_case(monkeypatch, capfd):
    """Test SubtractCommand with edge cases like zero or negative numbers."""
    monkeypatch.setattr('builtins.input', lambda _: '0 -7')  # Example: '0' and '-7'

    subtract_command = SubtractCommand()
    subtract_command.execute('0', '-7')  # Simulate subtracting 0 and -7

    captured = capfd.readouterr()
    assert "The result of 0 - -7 is 7" in captured.out

def test_multiply_command_valid_input(monkeypatch, capfd):
    """Test MultiplyCommand with valid input."""
    # Simulate user input for valid numbers
    monkeypatch.setattr('builtins.input', lambda _: '5 4')  # Example: '5' and '4' are the inputs

    multiply_command = MultiplyCommand()
    multiply_command.execute('5', '4')  # Simulate multiplying 5 and 4

    captured = capfd.readouterr()
    assert "The result of 5 * 4 is 20" in captured.out

def test_multiply_command_invalid_input(monkeypatch, capfd):
    """Test MultiplyCommand with invalid input (non-numeric values)."""
    # Simulate user input with invalid numbers
    monkeypatch.setattr('builtins.input', lambda _: '5 xyz')  # 'xyz' is invalid

    multiply_command = MultiplyCommand()
    multiply_command.execute('5', 'xyz')  # Simulate multiplying 5 and 'xyz'

    captured = capfd.readouterr()
    assert "Invalid number input: 5 or xyz is not valid number." in captured.out

def test_multiply_command_edge_case(monkeypatch, capfd):
    """Test MultiplyCommand with edge cases like zero or negative numbers."""
    monkeypatch.setattr('builtins.input', lambda _: '0 -8')  # Example: '0' and '-8'

    multiply_command = MultiplyCommand()
    multiply_command.execute('0', '-8')  # Simulate multiplying 0 and -8

    captured = capfd.readouterr()
    assert "The result of 0 * -8 is 0" in captured.out

def test_divide_command_valid_input(monkeypatch, capfd):
    """Test DivideCommand with valid input."""
    # Simulate user input for valid numbers
    monkeypatch.setattr('builtins.input', lambda _: '10 2')  # Example: '10' and '2' are the inputs

    divide_command = DivideCommand()
    divide_command.execute('10', '2')  # Simulate dividing 10 by 2

    captured = capfd.readouterr()
    assert "The result of 10 / 2 is 5" in captured.out

def test_divide_command_invalid_input(monkeypatch, capfd):
    """Test DivideCommand with invalid input (non-numeric values)."""
    # Simulate user input with invalid numbers
    monkeypatch.setattr('builtins.input', lambda _: '10 abc')  # 'abc' is invalid

    divide_command = DivideCommand()
    divide_command.execute('10', 'abc')  # Simulate dividing 10 by 'abc'

    captured = capfd.readouterr()
    assert "Invalid number: 10 or abc is not a valid number." in captured.out

def test_divide_command_zero_division(monkeypatch, capfd):
    """Test DivideCommand when attempting to divide by zero."""
    monkeypatch.setattr('builtins.input', lambda _: '10 0')  # Example: '10' and '0'

    divide_command = DivideCommand()
    divide_command.execute('10', '0')  # Simulate dividing 10 by 0

    captured = capfd.readouterr()
    assert "An error occurred: Cannot divide by zero" in captured.out

def test_app_menu_command(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'menu' command."""
    # Mock user inputs
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Create app without starting REPL immediately
    app = App(start_repl=False)

    # Create and register a menu command for testing purposes
    class MenuCommand(Command):  # pylint: disable=too-few-public-methods
        """Menu command for displaying available commands."""        
        def __init__(self, command_handler):
            self.command_handler = command_handler

        def execute(self):
            """Display available commands"""
            print("Available commands:")
            for cmd_name in sorted(self.command_handler.commands.keys()):
                print(f"  - {cmd_name}")

    # Register the menu command directly for testing
    app.command_handler.register_command("menu", MenuCommand(app.command_handler))

    # Run the REPL with SystemExit handling
    with pytest.raises(SystemExit) as e:
        app.run_repl()
    # Capture and verify output
    captured = capfd.readouterr()
    assert "Available commands:" in captured.out, "Menu command output incorrect"
    # Verify exit message
    assert str(e.value) == "Exiting...", "The app did not exit with the expected message"
