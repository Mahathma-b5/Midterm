"""Manages a history of mathematical operations."""
from typing import List, Optional
from calculator.calculation import OperationRecord

class OperationHistory:
    """Manages a history of mathematical operations."""
    records: List[OperationRecord] = []

    @classmethod
    def add_record(cls, record: OperationRecord) -> None:
        """
        Add an operation record to the history.

        :param record: An instance of OperationRecord to be stored.
        """
        cls.records.append(record)

    @classmethod
    def get_all_records(cls) -> List[OperationRecord]:
        """
        Retrieve all stored operation records.

        :return: A list of all OperationRecord instances.
        """
        return cls.records

    @classmethod
    def get_last_record(cls) -> Optional[OperationRecord]:
        """
        Retrieve the most recent operation record.

        :return: The last OperationRecord if available, otherwise None.
        """
        return cls.records[-1] if cls.records else None

    @classmethod
    def clear_records(cls) -> None:
        """
        Remove all operation records from history.
        """
        cls.records.clear()
