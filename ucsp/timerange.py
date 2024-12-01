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
            raise ValueError("Start time must be less than end time")
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start} to {self.end}"

    def is_time_between(self, time: time):
        return time > self.start and time < self.end


def time_range_overlap(time_range1: TimeRange, time_range2: TimeRange):
    return time_range1.is_time_between(
        time_range2.start
    ) or time_range1.is_time_between(time_range2.end)