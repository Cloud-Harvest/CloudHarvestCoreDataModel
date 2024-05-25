from CloudHarvestCoreTasks.base import BaseTask, TaskStatusCodes
from .recordset import HarvestRecordSet


class RecordSetTask(BaseTask):
    """
    The RecordSetTask class is a subclass of the BaseTask class. It represents a task that operates on a record set.

    Attributes:
        recordset_name (HarvestRecordSet): The name of the record set this task operates on.
        function (str): The name of the function to be applied on the record set.
        arguments (dict): The arguments to be passed to the function.

    Methods:
        method(): Executes the function on the record set with the provided arguments and stores the result in the data attribute.
    """

    def __init__(self, recordset_name: HarvestRecordSet, function: str, arguments: dict, *args, **kwargs):
        """
        Constructs a new RecordSetTask instance.

        Args:
            recordset_name (HarvestRecordSet): The name of the record set this task operates on.
            function (str): The name of the function to be applied on the record set.
            arguments (dict): The arguments to be passed to the function.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.recordset_name = recordset_name
        self.function = function
        self.arguments = arguments

    def method(self):
        """
        Executes the function on the record set with the provided arguments and stores the result in the data attribute.

        Returns:
            self: Returns the instance of the RecordSetTask.
        """
        recordset = self.task_chain.get_variables_by_names(self.recordset_name)
        self.data = getattr(recordset, self.function)(**self.arguments)

        return self
