from timerange import DaysOfWeek, TimeRange


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

    def __str__(self):
        return f"{self.name} - {self.schedule}"
