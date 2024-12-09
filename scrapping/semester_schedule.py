from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import datetime, time
from dotenv import load_dotenv
import json
import os

load_dotenv()

uam_session_cookie = f"PHPSESSID={os.getenv("UAM_TOKEN")}"

req_headers = {
    "Host": "intrauam.autonoma.edu.co",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://intrauam.autonoma.edu.co/intrauam2/l/url/estudiantes/horario/dobleCarrera.php",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "28",
    "Origin": "https://intrauam.autonoma.edu.co",
    "Connection": "keep-alive",
    "Cookie": uam_session_cookie,
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
}


def get_schedule_by_subject(subject: str):
    subject = subject.upper()
    url = f"https://intrauam.autonoma.edu.co/intrauam2/l/url/docente/horarioAsignatura/editar_sel.php?letra={subject[0]}&periodo=1&ano=2025"
    response = requests.get(url, headers=req_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="datos")
        data = []
        headers = []
        for th in table.find_all("th"):
            headers.append(th.text.strip())
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            row_subject = cols[1].text.strip().split("-")[-1].strip()
            if row_subject == subject:
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)
        return headers, data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None, None


def get_semesters_schedules(semesters):
    semesters_schedules = []
    for semester in semesters:
        semester_schedule = []
        for subject in semester:
            headers, cols = get_schedule_by_subject(subject)
            if headers is not None and cols is not None:
                semester_schedule.append((subject, headers, cols))
        semesters_schedules.append(semester_schedule)
    return semesters_schedules


def print_semester_schedules(semesters_schedules):
    for i, semester_schedule in enumerate(semesters_schedules):
        print(f"Semester {i+1}")
        for subject, headers, cols in semester_schedule:
            print(f"Subject: {subject}")
            print(tabulate(cols, headers=headers, tablefmt="fancy_grid"))
            print()


def get_classrooms_from_schedules(semesters_schedules):
    classrooms = {}
    for semester_schedule in semesters_schedules:
        for subject, headers, cols in semester_schedule:
            for col in cols:
                classrooms[col[5]] = {
                    "name": col[5],
                }
    return classrooms


def parse_session_schedule_time_range(
    time_range_str: str,
) -> Tuple[datetime, datetime] | None:
    # if there is no time range, return None
    if time_range_str.strip() == ": - :":
        return None
    splitted_str = time_range_str.split(" ")
    start = datetime.strptime(splitted_str[1], "%H:%M")
    end = datetime.strptime(splitted_str[3], "%H:%M")
    return start, end


def get_courses_from_schedules(semesters_schedules):
    courses = {}
    for i, semester_schedule in enumerate(semesters_schedules):
        for subject, headers, cols in semester_schedule:
            for col in cols:
                course_key = f"{subject} {col[1]} {col[2]}"
                time_range = parse_session_schedule_time_range(col[4])
                course = courses.get(course_key, None)
                if course is None:
                    course = {
                        "name": course_key,
                        "semester": i + 1,
                        "subject": subject,
                        "sessions": [
                            {
                                "duration": (
                                    str(time_range[1] - time_range[0])
                                    if time_range is not None
                                    else -1
                                ),
                            }
                        ],
                    }
                    courses[course_key] = course
                else:
                    time_range = parse_session_schedule_time_range(col[4])
                    course["sessions"].append(
                        {
                            "duration": (
                                str(time_range[1] - time_range[0])
                                if time_range is not None
                                else -1
                            ),
                        }
                    )
    return courses


"""
    creates a json file and store it in the system with the data of the courses given the schedules of the semesters
"""


def create_json_input_data(path: str, courses: List[dict], classrooms: List[dict]):
    with open(path, "w+") as file:
        json.dump({"courses": courses, "classrooms": classrooms}, file)


def main():
    semesters = [
        [
            "metodos numericos",
            "ecuaciones diferenciales",
            "paradigmas de lenguajes",
            "programacion back end",
            "redes lan",
            "ingenieria del software II",
        ],
        [
            "electricidad y magnetismo",
            "estadistica y probabilidad",
            "calculo vectorial",
            "bases de datos I",
            "sistemas operativos (tecnologia II)",
            "ingenieria de software I",
        ],
        [
            "fisica mecanica",
            "calculo integral",
            "matematicas discretas",
            "estructura de datos",
            "programacion orientada a objetos",
            "ingles III",
        ],
    ]

    semesters_schedules = get_semesters_schedules(semesters)
    print_semester_schedules(semesters_schedules)
    semesters_classrooms = get_classrooms_from_schedules(semesters_schedules)
    semesters_courses = get_courses_from_schedules(semesters_schedules)
    create_json_input_data(
        "uam_input_data.json",
        list(semesters_courses.values()),
        list(semesters_classrooms.values()),
    )


if __name__ == "__main__":
    main()
