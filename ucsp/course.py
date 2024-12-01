from typing import List
from session import Session
from timerange import TimeRange
from professor import Professor


class Course:

    def __init__(
        self,
        name: str,
        potential_professors: List[Professor],
        semester: int,
        quotas: int,
        sessions: List[Session],
        study_time: TimeRange | None = None,  # jornada academica
    ):
        self.name = name
        self.potential_professors = potential_professors
        self.semester = semester
        self.quotas = quotas
        self.study_time = study_time
        self.sessions = sessions

    def __str__(self):
        return f"{self.name} with {self.potential_professors} with sessions :\n {self.sessions}"
