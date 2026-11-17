# test_services.py
import pytest
from services import CourseService # מייבאים את המחלקה שאנו בודקים

# 1. יצירת "בסיס נתונים מזויף" לבדיקה
MOCK_DB_FOR_TESTS = {
    "cs": [
        {"id": "101", "name": "Intro", "prereqs": []},
    ],
    "math": [
        {"id": "901", "name": "Calculus", "prereqs": []},
    ]
}

# 2. שימוש ב-Fixture של PyTest:
# זהו "Setup" שרץ לפני כל פונקציית בדיקה ומכין לה את הסביבה.
@pytest.fixture
def service():
    """יוצר מופע חדש של CourseService עם ה-DB המזויף"""
    # מזריקים את ה-DB המזויף, לא את האמיתי מ-data.py!
    service = CourseService(db=MOCK_DB_FOR_TESTS)
    return service

# 3. כתיבת הבדיקה הראשונה
# שם הפונקציה חייב להתחיל ב-test_
def test_find_courses_by_dept_success(service):
    # ARRANGE (הכנה) - נעשה ע"י ה-fixture

    # ACT (פעולה)
    courses = service.find_courses_by_dept("cs")

    # ASSERT (בדיקה)
    assert courses is not None
    assert len(courses) == 1
    assert courses[0]["name"] == "Intro"

# 4. כתיבת בדיקת "מקרה קצה"
def test_find_courses_by_dept_not_found(service):
    # ARRANGE

    # ACT
    courses = service.find_courses_by_dept("physics")

    # ASSERT
    assert courses is None # מצפים לקבל None

def test_get_formatted_prereqs_empty(service):
    # ARRANGE
    course = MOCK_DB_FOR_TESTS["cs"][0] # הקורס "Intro"

    # ACT
    prereqs_str = service.get_formatted_prereqs(course)

    # ASSERT
    assert prereqs_str == "None"
