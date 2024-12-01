"""
ClassRooms class reprensent a classroom in an institution
:param name: name of the classroom
:param capacity: capacity of the classroom
:param classroom_type: index of the type of the classroom defined by the user.
"""


class ClassRoom:

    def __init__(self, name: str, capacity: int, classroom_type: int):
        self.name = name
        self.capacity = capacity
        self.classroom_type = classroom_type

    def __str__(self):
        return f"Classroom {self.name} with capacity {self.capacity} and type {self.classroom_type}"
