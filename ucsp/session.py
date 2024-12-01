from datetime import time
from timerange import TimeRange
from professor import Professor
from classroom import ClassRoom


class Session:

    def __init__(
        self,
        classroom_type: int,  # for example 0: theory, 1: laboratory
        duration: int,  # duration in hours
        day=None,
        professor: Professor | None = None,
        classroom: ClassRoom | None = None,
    ):
        self.classroom_type = classroom_type
        self.duration = duration
        self.day = day
        self.time_range = None
        self.professor = professor
        self.classroom = classroom

    def __str__(self):
        return f"{self.day} in {self.time_range} with {self.professor} in {self.classroom} of type {self.classroom_type}"

    def set_time_range(self, initial_time: time, final_time: time):
        self.time_range = TimeRange(initial_time, final_time)
        return self
