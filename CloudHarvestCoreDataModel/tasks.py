from CloudHarvestCoreTasks.base import BaseTask, TaskStatusCodes
from CloudHarvestCorePluginManager.decorators import register_definition
from .recordset import HarvestRecordSet
from typing import List


@register_definition(name='recordset')
class HarvestRecordSetTask(BaseTask):
    """
    The HarvestRecordSetTask class is a subclass of the BaseTask class. It represents a task that operates on a record set.

    Attributes:
        recordset_name (HarvestRecordSet): The name of the record set this task operates on.
        stages: A list of dictionaries containing the function name and arguments to be applied to the recordset.
        >>> stages = [
        >>>     {
        >>>         'function_name': {
        >>>             'argument1': 'value1',
        >>>             'argument2': 'value2'
        >>>         }
        >>>     }
        >>> ]

    Methods:
        method(): Executes the function on the record set with the provided arguments and stores the result in the data attribute.
    """

    def __init__(self, recordset_name: HarvestRecordSet, stages: List[dict], *args, **kwargs):
        """
        Constructs a new HarvestRecordSetTask instance.

        Args:
            recordset_name (HarvestRecordSet): The name of the record set this task operates on.
            stages (List[dict]): A list of dictionaries containing the function name and arguments to be applied to the recordset.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.recordset_name = recordset_name
        self.stages = stages
        self.position = 0

    def method(self):
        """
        Executes functions on the recordset with the provided function and arguments, then stores the result in the data attribute.

        This method iterates over the `stages` defined for this task. For each stage, it retrieves the function and its arguments.
        It then checks if the function is a method of the HarvestRecordSet or HarvestRecord class. If it is, it applies the function to the record set or each record in the record set, respectively.
        If the function is not a method of either class, it raises an AttributeError.

        The result of applying the function is stored in the data attribute of the HarvestRecordSetTask instance.

        Returns:
            self: Returns the instance of the HarvestRecordSetTask.
        """

        from .record import HarvestRecord
        from .recordset import HarvestRecordSet

        # Get the recordset from the task chain variables
        recordset = self.task_chain.get_variables_by_names(self.recordset_name).get(self.recordset_name)

        for stage in self.stages:
            # Record the position of stages completed
            self.position += 1

            # Each dictionary should only contain one key-value pair
            for function, arguments in stage.items():

                # This is a HarvestRecordSet command
                if hasattr(HarvestRecordSet, function):
                    getattr(recordset, function)(**arguments or {})

                # This is a HarvestRecord command
                elif hasattr(HarvestRecord, function):
                    [
                        getattr(record, function)(**arguments or {})
                        for record in recordset
                    ]

                else:
                    raise AttributeError(f"Neither HarvestRecordSet nor HarvestRecord has a method named '{function}'")

                break

        self.data = recordset

        return self
