"""
    Represents a UCSP (University Class Scheduling Problem) which is a particular CSP.
"""

from typing import List
from classroom import ClassRoom
from csp import CSP
from professor import Professor
from session import Session
from timerange import DaysOfWeek, TimeRange


class UCSP(CSP):

    def __init__(
        self,
        variables: List[Session],
        study_times: List[TimeRange],
        days: List[DaysOfWeek],
        classrooms: List[ClassRoom],
        professors: List[Professor],
    ):
        super().__init__(variables)
        self.domains = {}
        self.constraints = {}
        # This represents the domain of the subvariables of the CSP definition.
        self.study_times = study_times
        self.days = days
        self.classrooms = classrooms
        self.professors = professors

    def get_domain(self, variable):
        return self.domains[variable]

    def check_constraints(self, variable):
        return self.constraints[variable]
