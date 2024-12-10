import argparse
import os
import json
from professor import Professor
from timerange import TimeRange
from classroom import ClassRoom
from session import Session, Course
from ucsp import UCSP
from localsearch import LocalSearch
from datetime import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Nombre del archivo con los datos", type=str)
    args = parser.parse_args()
    if args.filename is None:
        print("Debe ingresar un archivo")
        return
    if args.filename is not None and not os.path.exists(args.filename):
        print("El archivo no existe")
        return
    with open(os.path.join(os.getcwd(), args.filename), "r+") as file:
        data = json.load(file)

    # Professors
    professors_list = []
    for professor in data["professors"]:
        schedule_dict = {}
        for key, value in professor["schedule"].items():
            schedule_dict[key] = [
                TimeRange(time(int(time_range["start"])), time(int(time_range["end"])))
                for time_range in value
            ]
        professors_list.append(Professor(professor["name"], schedule_dict))

    # Classrooms
    classrooms_list = [
        ClassRoom(classroom["name"], classroom["capacity"], classroom["type"])
        for classroom in data["classrooms"]
    ]

    # Classrooms types
    classrooms_types = data["classrooms_types"]

    # Days
    days = data["days"]

    # Study times
    study_times = [
        TimeRange(time(int(time_range["start"])), time(int(time_range["end"])))
        for time_range in data["study_times"]
    ]

    # Courses and Sessions
    courses_list = []
    sessions_list = []

    # Courses to be assigned
    for course in data["courses"]:
        study_time = course.get("study_time", None)
        obj_course = Course(
            name=course["name"],
            potential_professors=[
                professors_list[professors_list.index(professor)]
                for professor in course["potential_professors"]
            ],
            semester=course["semester"],
            subject=course["subject"],
            quotas=course["quotas"],
            study_time=study_times[study_time] if study_time is not None else None,
        )

        course_sessions = []
        for session in course["sessions"]:
            session = Session(
                classroom_type=session["classroom_type"],
                duration=session["duration"],
                course=obj_course,
            )
            sessions_list.append(session)
            course_sessions.append(session)
        obj_course.sessions = course_sessions
        courses_list.append(obj_course)

    # Fixed courses
    for fixed_course in data["fixed_courses"]:
        study_time = fixed_course.get("study_time", None)
        obj_course = Course(
            name=fixed_course["name"],
            potential_professors=[],
            semester=fixed_course["semester"],
            subject=fixed_course["subject"],
            quotas=fixed_course["quotas"],
            study_time=study_times[study_time] if study_time is not None else None,
            fixed=True,
        )

        course_sessions = []
        for session in fixed_course["sessions"]:
            classroom = next(
                (
                    classroom
                    for classroom in classrooms_list
                    if classroom.name == session["classroom"]
                ),
                None,
            )
            professor = next(
                (
                    professor
                    for professor in professors_list
                    if professor.name == fixed_course["professor"]
                ),
                None,
            )
            session_obj = Session(
                classroom_type=classroom.classroom_type,
                duration=session["duration"],
                day=session["day"],
                professor=professor,
                classroom=classroom,
                course=obj_course,
            )
            session_obj.set_time_range(
                time(int(session["start"])),
                time(int(session["start"]) + session["duration"]),
            )
            sessions_list.append(session_obj)
            course_sessions.append(session_obj)
        obj_course.sessions = course_sessions
        courses_list.append(obj_course)

    ucsp = UCSP(
        variables=sessions_list,
        study_times=study_times,
        days=days,
        classrooms=classrooms_list,
        professors=professors_list,
        classrooms_types=classrooms_types,
        courses=courses_list,
    )

    local_search = LocalSearch(ucsp)
    local_search.solve()


if __name__ == "__main__":
    main()
