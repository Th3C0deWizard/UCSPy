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
        fixed: bool = False,
    ):
        self.name = name
        self.potential_professors = potential_professors
        self.semester = semester
        self.subject = subject
        self.quotas = quotas
        self.study_time = study_time
        self.sessions = sessions
        self.no_overlap_courses = no_overlap_courses
        self.fixed = fixed

    def __str__(self):
        message = f"\n{self.name}\t| {self.quotas} quotas\t| {self.semester} semester\nProfessor: {self.sessions[0].professor.name}\n"
        for i, session in enumerate(self.sessions):
            message += f"Session {i + 1}: {session}\n"

        return message

    def __repr__(self) -> str:
        return self.__str__()
