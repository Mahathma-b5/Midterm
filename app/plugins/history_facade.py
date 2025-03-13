"""Facade pattern implementation for history management operations."""
import logging
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from calculator.calculation import OperationRecord
from calculator.history.history import OperationHistory
from calculator.operations import add_numbers, div_numbers, mul_numbers, sub_numbers
import logging
import logging.config

load_dotenv()
logger = logging.getLogger(__name__)


class HistoryFacade:
    """Facade for managing calculation history operations 
    including storage, retrieval, and persistence."""
    @staticmethod
    def _get_history_dir() -> Path:
        """Get history directory from environment variable, create if needed."""
        history_dir = Path(os.getenv('HISTORY_PATH', 'calculator_history'))
        logger.debug("Using history directory: %s", history_dir)
        try:
            history_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Created history directory at %s", history_dir.absolute())
        except PermissionError as pe:
            logger.critical("Permission denied creating history directory: %s", pe)
            raise RuntimeError(f"Permission denied creating history directory: {pe}") from pe
        return history_dir

    @staticmethod
    def get_formatted_history():
        """Get history with human-readable formatting."""
        logger.debug("Formatting calculation history")
        return [
            f"{record.x} {record.symbol} {record.y} = {record.execute()}"
            for record in OperationHistory.get_all_records()
        ]
    @staticmethod
    def clear_history():
        """Clear operation history."""
        logger.info("Clearing operation history")
        OperationHistory.clear_records()
    @staticmethod
    def get_last_formatted() -> str:
        """Get formatted last operation."""
        logger.debug("Retrieving last formatted operation")
        record = OperationHistory.get_last_record()
        if not record:
            logger.warning("No operations found in history")
            return "No operations in history"
        return f"{record.x} {record.symbol} {record.y} = {record.execute()}"
    @staticmethod
    def save_to_csv():
        """Save history with timestamped filename to configured directory."""
        history_dir = HistoryFacade._get_history_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"calculator_history_{timestamp}.csv"
        filepath = history_dir / filename
        records = OperationHistory.get_all_records()
        if not records:
            logger.warning("Attempted to save empty history")
            return "No history to save"
        logger.info("Saving %d records to %s", len(records), filepath)
        df = pd.DataFrame([{
            'operand1': str(r.x),
            'operand2': str(r.y),
            'operation': r.symbol,
            'result': str(r.execute())
        } for r in records])
        df.to_csv(filepath, index=False)
        logger.debug("CSV file created successfully at %s", filepath)
        return f"History saved to {filepath.absolute()}"
    @staticmethod
    def list_csv_files():
        """List all CSV files in history directory."""
        try:
            history_dir = HistoryFacade._get_history_dir()
            files = [f for f in history_dir.glob('*.csv') if f.is_file()]
            logger.debug("Found %d CSV files in history directory", len(files))
            return files
        except OSError as e:
            logger.error("Error listing CSV files: %s", str(e))
            return []
    @staticmethod
    def load_from_csv(filename: str) -> str:
        """Load history from CSV and return formatted entries."""
        try:
            logger.info("Attempting to load history from %s", filename)
            history_dir = HistoryFacade._get_history_dir()
            filepath = history_dir / filename
            if not filepath.exists():
                logger.error("CSV file not found: %s", filepath)
                return f"Error: File '{filepath}' not found"
            df = pd.read_csv(
                filepath,
                usecols=['operand1', 'operand2', 'operation', 'result']
            )
            OperationHistory.clear_records()
            logger.info("Cleared existing history before import")
            operation_map = {
                '+': add_numbers,
                '-': sub_numbers,
                '×': mul_numbers,
                '÷': div_numbers
            }
            loaded_count = 0
            for _, row in df.iterrows():
                try:
                    x = Decimal(str(row['operand1']))
                    y = Decimal(str(row['operand2']))
                    op_func = operation_map[row['operation']]
                    record = OperationRecord.create(x, y, op_func)
                    OperationHistory.add_record(record)
                    loaded_count += 1
                except (KeyError, ValueError, InvalidOperation) as e:
                    logger.warning("Skipping invalid record: %s - Error: %s", row.to_dict(), str(e))
                    continue
            formatted = HistoryFacade.get_formatted_history()
            logger.info("Successfully loaded %d records from %s", loaded_count, filename)
            result = [f"Loaded {loaded_count} entries from '{filename}':"]
            result += [f"{i+1}. {entry}" for i, entry in enumerate(formatted)]
            return "\n".join(result)
        except pd.errors.EmptyDataError:
            logger.error("Attempted to load empty CSV file")
            return "Error: CSV file is empty"
        except pd.errors.ParserError as e:
            logger.error("CSV parsing failed: %s", str(e))
            return "Error: Invalid CSV format"
        except KeyError as e:
            logger.error("Missing required column: %s", str(e))
            return f"Error: Missing column {str(e)}"
        except (OSError, RuntimeError) as e:
            logger.error("System error during loading: %s", str(e))
            return f"Loading failed: {str(e)}"
        
