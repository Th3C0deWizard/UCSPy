from datetime import time
from timerange import TimeRange
from professor import Professor
from classroom import ClassRoom
from course import Course


class Session:

    def __init__(
        self,
        classroom_type: int,  # for example 0: theory, 1: laboratory
        duration: int,  # duration in hours
        day=None,
        professor: Professor | None = None,
        classroom: ClassRoom | None = None,
        course: Course | None = None,
    ):
        self.classroom_type = classroom_type
        self.duration = duration
        self.day = day
        self.time_range: TimeRange | None = None
        self.professor = professor
        self.classroom = classroom
        self.course = course

    def __str__(self):
        return f"{self.course.name} with {self.course.quotas} quotas at {self.day} in {self.time_range} with {self.professor} in {self.classroom} - Real type {self.classroom_type}"

    def __repr__(self) -> str:
        return self.__str__()

    def set_time_range(self, initial_time: time, final_time: time):
        self.time_range = TimeRange(initial_time, final_time)
        return self
