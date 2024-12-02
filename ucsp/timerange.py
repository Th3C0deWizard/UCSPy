from datetime import time
from enum import Enum


class DaysOfWeek(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class TimeRange:
    def __init__(self, start: time, end: time):
        if start > end:
            raise ValueError(
                f"Start time must be less than end time. Start: {start}, End: {end}"
            )
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start} to {self.end}"

    def __repr__(self) -> str:
        return self.__str__()

    def is_time_between(self, time: time):
        return time > self.start and time < self.end

    def is_complete_inside_range(self, time_range: "TimeRange"):
        return time_range.start <= self.start and time_range.end >= self.end

    def get_duration(self):
        return self.end.hour - self.start.hour


def time_range_overlap(time_range1: TimeRange, time_range2: TimeRange):
    return time_range1.is_time_between(
        time_range2.start
    ) or time_range1.is_time_between(time_range2.end)
