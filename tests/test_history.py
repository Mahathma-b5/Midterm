"""History Testing File"""
from decimal import Decimal
from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from app.plugins.history_facade import HistoryFacade
from calculator.calculation import OperationRecord # type: ignore
from calculator.history.history import OperationHistory
from calculator.operations import add_numbers, sub_numbers, mul_numbers, div_numbers # type: ignore

# Ensure `clear_records()` is defined in OperationHistory
if not hasattr(OperationHistory, 'clear_records'):
    @classmethod
    def clear_records(cls):
        """Clear all operation history records."""
        cls._records = []
    OperationHistory.clear_records = clear_records

@pytest.fixture(autouse=True)
def clear_history_before_tests():
    """Automatically clear operation history before each test to ensure a clean state."""
    OperationHistory.clear_records()

@pytest.fixture
def sample_operations():
    """Create a set of sample operations for testing history functionality."""
    return [
        OperationRecord.create(Decimal('10'), Decimal('5'), add_numbers),
        OperationRecord.create(Decimal('20'), Decimal('4'), sub_numbers),
        OperationRecord.create(Decimal('3'), Decimal('7'), mul_numbers),
        OperationRecord.create(Decimal('100'), Decimal('20'), div_numbers)
    ]

def test_get_formatted_history(sample_operations):  # pylint: disable=redefined-outer-name
    """Test that the history facade correctly formats the operation history."""
    for operation in sample_operations:
        OperationHistory.add_record(operation)
    formatted = HistoryFacade.get_formatted_history()
    assert formatted == [
        "10 + 5 = 15",
        "20 - 4 = 16",
        "3 × 7 = 21",
        "100 ÷ 20 = 5"
    ]

def test_clear_history(sample_operations):  # pylint: disable=redefined-outer-name
    """Test that the history facade can clear all operation records."""
    for operation in sample_operations:
        OperationHistory.add_record(operation)
    HistoryFacade.clear_history()
    assert len(OperationHistory.get_all_records()) == 0

def test_get_last_formatted(sample_operations):  # pylint: disable=redefined-outer-name
    """Test retrieving the last formatted operation from history."""
    assert HistoryFacade.get_last_formatted() == "No operations in history"
    for operation in sample_operations:
        OperationHistory.add_record(operation)
    assert HistoryFacade.get_last_formatted() == "100 ÷ 20 = 5"

# Correct mocking of file operations
@patch('app.plugins.history_facade.pd.DataFrame.to_csv')
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_save_to_csv(mock_get_dir, mock_to_csv, sample_operations, tmp_path):  # pylint: disable=redefined-outer-name
    """Test saving operation history to a CSV file."""
    mock_get_dir.return_value = tmp_path
    for operation in sample_operations:
        OperationHistory.add_record(operation)

    result = HistoryFacade.save_to_csv()
    mock_to_csv.assert_called_once()
    assert "History saved to" in result

# Convert PosixPath objects to strings for comparison
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_list_csv_files(mock_get_dir, tmp_path):
    """Test listing available CSV history files."""
    mock_get_dir.return_value = tmp_path
    fake_file1 = tmp_path / 'history1.csv'
    fake_file2 = tmp_path / 'history2.csv'
    fake_file1.touch()
    fake_file2.touch()

    files = HistoryFacade.list_csv_files()
    assert set(map(str, files)) == {str(fake_file1), str(fake_file2)}

@patch('app.plugins.history_facade.pd.read_csv')
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_load_from_csv(mock_get_dir, mock_read_csv, tmp_path):
    """Test loading operation history from a CSV file."""
    mock_get_dir.return_value = tmp_path
    csv_file = tmp_path / "test.csv"
    csv_file.touch()

    mock_df = MagicMock()
    mock_df.iterrows.return_value = iter([
        (0, {'operand1': '8', 'operand2': '2', 'operation': '+', 'result': '10'}),
        (1, {'operand1': '9', 'operand2': '3', 'operation': '-', 'result': '6'}),
        (2, {'operand1': '4', 'operand2': '5', 'operation': '×', 'result': '20'}),
        (3, {'operand1': '100', 'operand2': '25', 'operation': '÷', 'result': '4'})
    ])
    mock_read_csv.return_value = mock_df
    result = HistoryFacade.load_from_csv("test.csv")

    expected_output_lines = [
        "Loaded 4 entries from 'test.csv':",
        "1. 8 + 2 = 10",
        "2. 9 - 3 = 6",
        "3. 4 × 5 = 20",
        "4. 100 ÷ 25 = 4"
    ]
    assert result == "\n".join(expected_output_lines)

@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_load_from_csv_file_not_found(mock_get_dir, tmp_path):
    """Test handling of non-existent CSV files when loading history."""
    mock_get_dir.return_value = tmp_path
    non_existing_file = "nonexistent.csv"

    result = HistoryFacade.load_from_csv(non_existing_file)

    assert result == f"Error: File '{tmp_path / non_existing_file}' not found"

@patch('app.plugins.history_facade.pd.read_csv', side_effect=pd.errors.EmptyDataError)
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_load_from_empty_csv(mock_get_dir, _mock_read_csv, tmp_path):
    '''Test handling of empty CSV files when loading history.'''
    mock_get_dir.return_value = tmp_path
    empty_file = tmp_path / "empty.csv"
    empty_file.touch()

    result = HistoryFacade.load_from_csv("empty.csv")

    assert result == "Error: CSV file is empty"
