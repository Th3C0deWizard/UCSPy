"""
    Represents a UCSP (University Class Scheduling Problem) which is a particular CSP.
"""

from typing import List, Tuple, Any, cast
from classroom import ClassRoom
from csp import CSP
from professor import Professor
from session import Session
from timerange import DaysOfWeek, TimeRange, time_range_overlap
from datetime import time
from course import Course
import random
import copy


class UCSP(CSP):

    def __init__(
        self,
        variables: List[Session],
        study_times: List[TimeRange],
        days: List[DaysOfWeek],
        classrooms: List[ClassRoom],
        professors: List[Professor],
        classrooms_types: List[str],
        courses: List[Course],
    ):
        super().__init__(variables)
        self.domains = {}  # Not used
        self.constraints = {}  # Not used
        # This represents the domain of the subvariables of the CSP definition.
        self.study_times = study_times
        self.days = days  # Not used
        self.classrooms = classrooms
        self.professors = professors  # Not used
        self.classrooms_types = classrooms_types  # Not used
        self.courses = courses

    def assign_random_value(self, variable: Session):
        """
        Assigns a random value to a variable.
        """
        if variable.course.fixed:
            return

        possible = False

        # for professor in variable.course.potential_professors:
        #     variable.professor = professor
        #     variable.day = random.choice(list(variable.professor.schedule.keys()))
        #     schedule = variable.professor.available_schedule.get(variable.day, None)
        #     duration = variable.duration
        #     for sch in schedule:
        #         time_sch = copy.deepcopy(sch)
        #         if time_sch.start.minute > 0 and time_sch.start.minute < 30:
        #             time_sch.start = time_sch.start.replace(minute=30)
        #         elif time_sch.start.minute > 30:
        #             time_sch.start = time_sch.start.replace(
        #                 hour=time_sch.start.hour + 1, minute=0
        #             )

        #         if time_sch.get_duration() >= duration:
        #             variable.time_range = TimeRange(
        #                 time_sch.start,
        #                 time_sch.start.replace(hour=time_sch.start.hour + duration),
        #             )
        #             new_range = TimeRange(variable.time_range.start, time_sch.end)
        #             if new_range.get_duration() > 0:
        #                 schedule.insert(schedule.index(sch), new_range)
        #             schedule.remove(sch)
        #             break

        #     if variable.time_range is not None:
        #         possible = True
        #         break

        if not possible:
            variable.professor = random.choice(self.professors)
            variable.day = random.choice(self.days)
            study_time = random.choice(self.study_times)
            start = random.choice(
                range(study_time.start.hour, study_time.end.hour - variable.duration)
            )
            variable.time_range = TimeRange(
                time(start), time(start + variable.duration)
            )

        possible_classrooms = [
            classroom
            for classroom in self.classrooms
            if classroom.classroom_type == variable.classroom_type
        ]

        variable.classroom = random.choice(possible_classrooms)

    def is_solved(self) -> Tuple[List[Tuple[Session, int]], bool]:
        constraints = []
        for variable in self.variables:
            if variable.course.fixed:
                continue
            constraints.append((variable, self.check_constraints(variable)))
        constraints.sort(reverse=True, key=lambda x: x[1])
        return constraints, constraints[0][1] == 0

    def check_constraints(self, variable: Session):
        constraints = 0

        # Unary constraints

        """
        Para la asignación de una sesión la combinación de las sub-variables día, hora de inicio y hora de fin debe pertenecer 
        al conjunto de horarios disponibles del profesor asignado.
        """
        if variable.professor.schedule.get(variable.day, None) is not None:
            times = variable.professor.schedule[variable.day]
            valid_time = False
            for time in times:
                if variable.time_range.is_complete_inside_range(time):
                    valid_time = True
                    break
            if not valid_time:
                constraints += 1
        else:
            constraints += 1

        """
        Para la asignación de una sesión, la sub-variable salón debe ser del tipo de salón del curso, si aplica.
        """
        if variable.classroom_type != variable.classroom.classroom_type:
            constraints += 1

        """
        Para la asignación de una sesión, la sub-variable salón debe tener capacidad mayor o igual a la cantidad de cupos del curso.
        """
        if variable.classroom.capacity < variable.course.quotas:
            constraints += 1

        """
        Para la asignación de una sesión, el rango entre la hora de inicio y la hora de fin debe estar dentro del rango de la jornada del curso, si tiene.
        """
        if (
            variable.course.study_time is not None
            and not variable.time_range.is_complete_inside_range(
                variable.course.study_time
            )
        ):
            constraints += 1

        """
        Para la asignación de una sesión, el profesor asignado debe ser el mismo para todas las sesiones del mismo curso.
        """
        sessions = variable.course.sessions
        for session in sessions:
            if session.professor.name != variable.professor.name:
                constraints += 1
                break

        # Binary constraints
        for v in cast(List[Session], self.variables):
            if v == variable:
                continue

            """
            Si para las asignaciones de dos sesiones de cursos sobre diferentes asignaturas que se ven en el mismo semestre 
            la sub-variable día es igual, entonces se debe cumplir que el rango entre la hora de inicio y la de fin, de cada sesión, 
            no se puede cruzar.
            """

            if (
                v.course.subject != variable.course.subject
                and v.course.semester == variable.course.semester
                and v.day == variable.day
                and time_range_overlap(v.time_range, variable.time_range)
            ):
                courses_subject = [
                    course
                    for course in self.courses
                    if course.subject == v.course.subject and course != v.course
                ]

                if len(courses_subject) > 0:
                    overlap = True
                    for course in courses_subject:
                        course_overlap = False
                        for session in course.sessions:
                            if session.day == variable.day:
                                if time_range_overlap(
                                    session.time_range, variable.time_range
                                ):
                                    course_overlap = True
                                    break
                        if not course_overlap:
                            overlap = False
                            break
                    if overlap:
                        constraints += 1
                else:
                    constraints += 1

            """
            Si para las asignaciones de dos sesiones de cursos sobre diferentes asignaturas que no se pueden cruzar de acuerdo a la 
            definición del problema la sub-variable día es igual, entonces se debe cumplir que el rango entre la hora de inicio y la 
            de fin, de cada sesión, no se puede cruzar.
            """
            if (
                variable.course.no_overlap_courses
                and v in variable.course.no_overlap_courses
                and v.day == variable.day
                and time_range_overlap(v.time_range, variable.time_range)
            ):
                constraints += 1

            """
            Si para las asignaciones de dos sesiones de cursos la combinación de las sub-variables día y profesor son iguales, 
            entonces se debe cumplir que el rango entre la hora de inicio y la de fin, de cada sesión, no se puede cruzar.
            """
            if (
                v.professor == variable.professor
                and v.day == variable.day
                and time_range_overlap(v.time_range, variable.time_range)
            ):
                constraints += 1

            """
            Para las asignaciones de dos sesiones del mismo curso, la sub-variable día debe ser diferente.
            """
            if variable.course == v.course and variable.day == v.day:
                constraints += 1

            """
            Si para las asignaciones de dos sesiones de cursos la combinación de las sub-variables día, hora de inicio y 
            hora de fin son iguales, entonces se debe cumplir que el salón sea diferente.
            """
            if (
                variable.day == v.day
                and time_range_overlap(v.time_range, variable.time_range)
                and variable.classroom == v.classroom
            ):
                constraints += 1

        return constraints

    def select_value_with_fewest_constraints(self, variable: Session):
        domain = {}
        duration = variable.duration
        for proffesor in variable.course.potential_professors:
            variable.professor = proffesor
            for day in proffesor.schedule.keys():
                variable.day = day
                for time_sch in proffesor.schedule[day]:
                    temp_time_range = copy.deepcopy(time_sch)
                    if time_sch.start.minute > 0:
                        temp_time_range.start = time_sch.start.replace(
                            hour=time_sch.start.hour + 1, minute=0
                        )

                    while temp_time_range.get_duration() >= duration:
                        for classroom in self.classrooms:
                            if classroom.classroom_type == variable.classroom_type:
                                variable_time_range = TimeRange(
                                    temp_time_range.start,
                                    temp_time_range.start.replace(
                                        hour=temp_time_range.start.hour + duration
                                    ),
                                )
                                temp_session = Session(
                                    variable.classroom_type,
                                    duration,
                                    day,
                                    proffesor,
                                    classroom,
                                    variable.course,
                                )
                                temp_session.time_range = variable_time_range
                                domain[temp_session] = self.check_constraints(
                                    temp_session
                                )

                        temp_time_range.start = temp_time_range.start.replace(
                            hour=temp_time_range.start.hour + 1
                        )

        # if the minimun number of constraints is the same as the current variable, then try to assign other variable with same number of constraints if posible
        sorted_constraints = sorted(domain.items(), key=lambda x: x[1])
        prev = sorted_constraints[0][1]
        min_session = sorted_constraints[0]
        for var, ctr in sorted_constraints:
            if prev != ctr:
                break
            if not self.are_equal(var, variable):
                min_session = (var, ctr)
                break
            prev = ctr

        # return min_session
        return None if self.are_equal(min_session[0], variable) else min_session

    def equals_variable(self, variable: Session, new_variable: Session):
        variable.day = new_variable.day
        variable.time_range = new_variable.time_range
        variable.professor = new_variable.professor
        variable.classroom = new_variable.classroom

    def are_equal(self, a: Session, b: Session):
        return (
            a.day == b.day
            and a.time_range == b.time_range
            and a.professor.name == b.professor.name
            and a.classroom.name == b.classroom.name
            and a.course.name == b.course.name
        )

    def print_solution(self):
        for course in self.courses:
            print(course)
            print("--------------------------------------------------")
