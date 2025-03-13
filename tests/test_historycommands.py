"""Tests for calculator history functionality."""

# Standard library imports
from decimal import Decimal

from pytest import CaptureFixture, MonkeyPatch

# Local application imports
from app.plugins.history_clear import HistoryClearCommand
from app.plugins.history_facade import HistoryFacade
from app.plugins.history_load import HistoryLoadCommand
from app.plugins.history_show import HistoryShowCommand
from app.plugins.last_operation import LastOpCommand # type: ignore
from calculator.calculation import OperationRecord # type: ignore
from calculator.history.history import OperationHistory
from calculator.operations import add_numbers # type: ignore


def test_history_clear_command():
    """Test that the history clear command properly clears all records."""
    # Add a dummy operation to history
    record = OperationRecord.create(Decimal('1'), Decimal('2'), add_numbers)
    OperationHistory.add_record(record)
    assert len(OperationHistory.get_all_records()) == 1

    # Execute the HistoryClearCommand
    command = HistoryClearCommand()
    command.execute()

    # Verify history is cleared
    assert len(OperationHistory.get_all_records()) == 0


def test_no_history():
    """Test behavior of HistoryFacade methods when there is no history."""
    OperationHistory.clear_records()
    assert HistoryFacade.get_formatted_history() == []
    assert HistoryFacade.get_last_formatted() == "No operations in history"
    assert HistoryFacade.save_to_csv() == "No history to save"


def test_history_show_command_no_history(capsys: CaptureFixture[str]):
    """Test HistoryShowCommand when no history exists."""
    # Ensure history is empty
    OperationHistory.clear_records()
    assert len(OperationHistory.get_all_records()) == 0

    # Execute HistoryShowCommand
    command = HistoryShowCommand()
    command.execute()

    # Capture printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == "No history available"


def test_history_last_command_no_history(capsys: CaptureFixture[str]):
    """Test LastOpCommand when no history exists."""
    # Ensure history is empty
    OperationHistory.clear_records()

    command = LastOpCommand()
    command.execute()

    captured = capsys.readouterr()
    assert captured.out.strip().lower() == "final operation: No operations in history".lower()

def test_history_last_command_with_history(capsys: CaptureFixture[str]):
    """Test LastOpCommand with an operation in history."""
    # Add a sample operation to history
    record = OperationRecord.create(Decimal('3'), Decimal('4'), add_numbers)
    OperationHistory.add_record(record)

    # Execute command
    command = LastOpCommand()
    command.execute()

    captured = capsys.readouterr()
    assert captured.out.strip().lower() == "final operation: 3 + 4 = 7".lower()



def test_history_load_command_no_files(capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
    """Test HistoryLoadCommand when no history files exist."""
    # Mock HistoryFacade.list_csv_files to return empty list
    monkeypatch.setattr(HistoryFacade, 'list_csv_files', lambda: [])
    # Execute the HistoryLoadCommand
    command = HistoryLoadCommand()
    command.execute()
    # Capture printed output
    captured = capsys.readouterr()
    assert "No history files found in current directory." in captured.out


def test_history_load_command_with_files(capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
    """Test HistoryLoadCommand with available history files."""
    # Mock file objects
    class MockFile:# pylint: disable=too-few-public-methods
        """Simple mock file object for testing."""
        def __init__(self, name):
            self.name = name
    mock_files = [MockFile("history1.csv"), MockFile("history2.csv")]
    # Mock HistoryFacade methods
    monkeypatch.setattr(HistoryFacade, 'list_csv_files', lambda: mock_files)
    monkeypatch.setattr(
        HistoryFacade,
        'load_from_csv', 
        lambda x: f"Successfully loaded {x}")
    # Mock user input to select the first file (index 1)
    input_values = ["1"]
    input_mock = lambda _: input_values.pop(0)# pylint: disable=unnecessary-lambda-assignment
    monkeypatch.setattr('builtins.input', input_mock)
    # Execute the command
    command = HistoryLoadCommand()
    command.execute()
    # Capture and verify output
    captured = capsys.readouterr()
    assert "Available history files:" in captured.out
    assert "1. history1.csv" in captured.out
    assert "2. history2.csv" in captured.out
    assert "Successfully loaded history1.csv" in captured.out


def test_history_load_command_with_invalid_selection(capsys: CaptureFixture[str],
                                                     monkeypatch: MonkeyPatch):
    """Test HistoryLoadCommand with invalid user input selections."""
    # Mock file objects with two files
    class MockFile:# pylint: disable=too-few-public-methods
        """Simple mock file object for testing."""
        def __init__(self, name):
            self.name = name
    mock_files = [MockFile("history1.csv"), MockFile("history2.csv")]
    # Mock HistoryFacade methods
    monkeypatch.setattr(HistoryFacade, 'list_csv_files', lambda: mock_files)
    monkeypatch.setattr(
        HistoryFacade,
        'load_from_csv',
        lambda x: f"Successfully loaded {x}")
    # Mock sequence of user inputs: invalid number, non-numeric, then valid selection
    input_values = ["3", "abc", "2"]
    input_mock = lambda _: input_values.pop(0)# pylint: disable=unnecessary-lambda-assignment
    monkeypatch.setattr('builtins.input', input_mock)
    # Execute the command
    command = HistoryLoadCommand()
    command.execute()
    # Capture and verify output
    captured = capsys.readouterr()
    assert "Invalid selection. Please enter a valid number." in captured.out
    assert "Please enter a numeric value." in captured.out
    assert "Successfully loaded history2.csv" in captured.out
