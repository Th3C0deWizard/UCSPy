from datetime import time
from timerange import DaysOfWeek, TimeRange, time_range_overlap
from session import Session


def main():
    session = Session(0, 2, DaysOfWeek.MONDAY, "John Doe", "Room 1")
    session.set_time_range(time(8, 0), time(10, 0))
    print(session.time_range.is_time_between(time(9)))
    print(time_range_overlap(session.time_range, TimeRange(time(10, 0), time(11, 0))))
    return


if __name__ == "__main__":
    main()
