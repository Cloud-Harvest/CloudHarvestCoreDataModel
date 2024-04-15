from typing import Dict, List, Literal
from .record import HarvestRecord


class HarvestRecordSet(List[HarvestRecord]):
    def __init__(self, data: List[Dict] = None, **kwargs):
        """
        Initialize a HarvestRecordSet object.

        :param data: A list of dictionaries to initialize the record set with, defaults to None
        :param kwargs: Additional keyword arguments
        """

        super().__init__(**kwargs)

        self.indexes = {}

        if data:
            self.add(data=data)

    def __enter__(self) -> 'HarvestRecordSet':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def __add__(self, other):
        self.add(data=other)

        return self

    @property
    def keys(self) -> List[str]:
        return sorted(list(set([key for record in self for key in record.keys()])))

    def add(self, data: List[dict or HarvestRecord]) -> 'HarvestRecordSet':
        """
        Add a list of records to the record set.

        :param data: A list of dictionaries or HarvestRecord objects to add to the record set. If the object is a
        dictionary, it will automatically be converted to a HarvestRecord.
        """

        [
            self.append(record)
            if isinstance(record, HarvestRecord)
            else self.append(HarvestRecord(**record))
            for record in data
        ]

        return self

    def add_match(self, syntax: str) -> 'HarvestRecordSet':
        """
        Add a match to the record set.

        :param syntax: The match syntax to add
        """

        [record.match(syntax) for record in self]

        return self

    def clear_matches(self) -> 'HarvestRecordSet':
        """
        Clear all matches from the record set.
        """

        [record.clear_matches() for record in self]

        return self

    def create_index(self, index_name: str, *fields: List[str]) -> 'HarvestRecordSet':
        """
        Create an index for the record set.

        :param index_name: The name of the index
        :param fields: The fields to include in the index

        """
        self.indexes[index_name] = {
            frozenset(record.get(field) for field in fields): record
            for record in self
        }

        return self

    def drop_index(self, index_name: str) -> 'HarvestRecordSet':
        """
        Drop an index from the record set.

        :param index_name: The name of the index to drop
        """

        self.indexes.pop(index_name)

        return self

    def get_matched_records(self) -> 'HarvestRecordSet':
        """
        Get all records in the record set that are a match.

        :return: A HarvestRecordSet object containing all matched records
        """

        return HarvestRecordSet(data=[record for record in self if record.is_matched_record])

    def modify_records(self, function: str, arguments: dict) -> 'HarvestRecordSet':
        """
        Modify records in the record set by calling a function on each record.

        :param function: The name of the function to call
        :param arguments: The arguments to pass to the function
        """

        [getattr(record, function)(**arguments) for record in self]

        return self

    def remove_duplicates(self) -> 'HarvestRecordSet':
        """
        Remove duplicate records from the record set.
        """

        unique_records = {
            frozenset(record.items()): record
            for record in self
        }

        self.clear()
        self.add(data=list(unique_records.values()))

        return self

    def remove_unmatched_records(self) -> 'HarvestRecordSet':
        """
        Remove all records in the record set that are not a match.
        """

        self[:] = [
            record for record in self
            if not record.is_matched_record
        ]

        return self

    def unwind(self, source_key: str, preserve_null_and_empty_keys: bool = True) -> 'HarvestRecordSet':
        """
        Unwind a list of records in the record set into separate records.

        :param source_key: The key of the list to unwind
        :param preserve_null_and_empty_keys: Whether to preserve keys with null or empty values, defaults to True
        """

        new_records = []
        for record in self:
            if source_key not in record and preserve_null_and_empty_keys is False:
                continue

            elif isinstance(record[source_key], (list or tuple)):
                for item in record[source_key]:
                    new_record = record.copy()
                    new_record[source_key] = item
                    new_records.append(new_record)

            else:
                new_records.append(record)

        self.clear()
        self.add(data=new_records)

        return self


class HarvestRecordSets(Dict[str, HarvestRecordSet]):

    def add(self, recordset_name: str, recordset: HarvestRecordSet) -> 'HarvestRecordSets':
        self[recordset_name] = recordset

        return self

    def index(self, recordset_name: str, index_name: str, fields: List[str]) -> 'HarvestRecordSets':
        return self

    def join(self, new_recordset_name: str, recordset_names: List[str], index_name: str, join_type: Literal['inner', 'outer', 'left', 'right']) -> 'HarvestRecordSets':
        return self

    def list(self) -> List[dict]:
        return [
            {
                'Name': name,
                'Keys': '\n'.join(recordset.keys),
                'Matches': len(recordset.get_matched_records()),
                'Total': len(recordset)
            }
            for name, recordset in self.items()
        ]

    def purge(self) -> 'HarvestRecordSets':
        self.clear()

        return self

    def query(self, recordset_name: str):
        return self.get(recordset_name)

    def remove(self, name: str) -> 'HarvestRecordSets':
        self.pop(name)
        return self

    def rename(self, old_recordset_name: str, new_recordset_name: str) -> 'HarvestRecordSets':
        self[new_recordset_name] = self.pop(old_recordset_name)

        return self
