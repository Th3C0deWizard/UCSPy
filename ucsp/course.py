from typing import List
from timerange import TimeRange
from professor import Professor


class Course:

    def __init__(
        self,
        name: str,
        potential_professors: List[Professor],
        semester: int,
        subject: str,
        quotas: int,
        sessions: List["Session"] | None = None,
        study_time: TimeRange | None = None,  # jornada academica
        no_overlap_courses: List["Course"] = None,
    ):
        self.name = name
        self.potential_professors = potential_professors
        self.semester = semester
        self.subject = subject
        self.quotas = quotas
        self.study_time = study_time
        self.sessions = sessions
        self.no_overlap_courses = no_overlap_courses

    def __str__(self):
        return f"{self.name} with {self.potential_professors}"

    def __repr__(self) -> str:
        return self.__str__()
