from typing import Dict, List
from record import HarvestRecord


class HarvestRecordSet(List[HarvestRecord]):
    def __init__(self, data: List[Dict] = None, **kwargs):
        super().__init__(**kwargs)

        if data:
            self.add(data=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def __add__(self, other):
        [self.append(record) for record in other]

        return self

    def add(self, data: List[dict or HarvestRecord]):
        [
            self.append(record)
            if isinstance(record, HarvestRecord)
            else self.append(HarvestRecord(**record))
            for record in data
        ]

        return self

    def record_operation(self, function: str, args: dict):
        """
        Allows the user to call a loop over the entire HarvestRecordSet to perform a HarvestRecord action.
        :param function: the name of the underlying function to call
        :param args: arguments for the RecordSet function
        :return:
        """

        [getattr(record, function)(**args) for record in self]

        return self


if __name__ == '__main__':
    test_data = [
        {
            "FieldA": "A",
            "FieldB": "B",
            "TagList": [
                {
                    "Name": "Something",
                    "Value": "Else"
                },
                {
                    "Name": "Another",
                    "Value": "Tag"
                }
            ]
        },
        {
            "FieldA": "A2",
            "FieldB": "B2",
            "TagList": [
                {
                    "Name": "Something2",
                    "Value": "Else2"
                },
                {
                    "Name": "Another2",
                    "Value": "Tag2"
                }
            ]
        }
    ]

    with HarvestRecordSet(data=test_data) as hrs:
        hrs.record_operation(function='name_value_to_dict',
                             args=dict(source_column='TagList',
                                       name_key='Name',
                                       value_key='Value',
                                       target_column='Tags',
                                       preserve_original=False))

        print(hrs)
