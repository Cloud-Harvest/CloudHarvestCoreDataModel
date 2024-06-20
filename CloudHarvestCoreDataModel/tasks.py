from CloudHarvestCoreTasks.base import BaseTask, TaskStatusCodes
from CloudHarvestCorePluginManager.decorators import register_definition
from .recordset import HarvestRecordSet


@register_definition
class RecordsetTask(BaseTask):
    """
    The RecordsetTask class is a subclass of the BaseTask class. It represents a task that operates on a record set.

    Attributes:
        recordset_name (HarvestRecordSet): The name of the record set this task operates on.
        function (str): The name of the function to be applied on the record set.
        arguments (dict): The arguments to be passed to the function.

    Methods:
        method(): Executes the function on the record set with the provided arguments and stores the result in the data attribute.
    """

    def __init__(self, recordset_name: HarvestRecordSet, function: str, arguments: dict, *args, **kwargs):
        """
        Constructs a new RecordsetTask instance.

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
            self: Returns the instance of the RecordsetTask.
        """
        from .record import HarvestRecord
        recordset = self.task_chain.get_variables_by_names(self.recordset_name).get(self.recordset_name)

        # This is a HarvestRecordSet command
        if hasattr(HarvestRecordSet, self.function):
            getattr(recordset, self.function)(**self.arguments)

        # This is a HarvestRecord command
        elif hasattr(HarvestRecord, self.function):
            [
                getattr(record, self.function)(**self.arguments)
                for record in recordset
            ]

        else:
            raise AttributeError(f"Neither HarvestRecordSet nor HarvestRecord has a method named '{self.function}'")

        self.data = recordset

        return self
