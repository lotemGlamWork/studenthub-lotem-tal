# test_data.py - STU-202: "חוזה הנתונים" (Data Contract)
#
# אלו לא בדיקות של לוגיקה, אלא של *הנתונים*.
# אם מישהו בצוות יוסיף מחר קורס בלי מחיר, או עם דרישת קדם לקורס שלא קיים,
# הבדיקה תיכשל עוד לפני שמשתמש יראה את הבעיה.
import pytest

from data import COURSES_DB

ALL_COURSES = [course for dept in COURSES_DB.values() for course in dept]
ALL_IDS = {course["id"] for course in ALL_COURSES}


@pytest.mark.parametrize("course", ALL_COURSES, ids=lambda c: c["id"])
def test_every_course_has_positive_price(course):
    assert isinstance(course.get("price"), (int, float))
    assert course["price"] > 0


def test_course_ids_are_unique():
    assert len(ALL_IDS) == len(ALL_COURSES)


@pytest.mark.parametrize("course", ALL_COURSES, ids=lambda c: c["id"])
def test_prereqs_refer_to_existing_courses(course):
    for prereq_id in course["prereqs"]:
        assert prereq_id in ALL_IDS
