from timerange import DaysOfWeek, TimeRange
import copy


class Professor:
    """
    Professor class constructor
    name: unique name of the professor
    schedule: dictionary of the professor's schedule
        the key is the day of the week (defined by the final users)
        the value is a list of TimeRange, each representing a time range
    """

    def __init__(self, name: str, schedule: dict[DaysOfWeek, list[TimeRange]]):
        self.name = name
        self.schedule = schedule
        self.available_schedule = copy.deepcopy(schedule)

    def __str__(self):
        return f"{self.name} - Schedule: {self.schedule}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value: str) -> bool:
        return self.name == value
