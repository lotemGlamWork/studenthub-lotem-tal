# main.py - V5: STU-202 - מחיר אמיתי לכל קורס
# מה השתנה מ-step-1?
#   הקבוע BASE_PRICE נמחק. כל קורס מגיע עם "price" משלו מ-data.py.
from data import COURSES_DB
from services import CourseService
from student import Student          # מייבאים את המחלקה, לא את המודול
from strategies import (
    IPricingStrategy,
    DefaultStrategy,
    FixedDiscountStrategy,
    PercentageDiscountStrategy,
)
from exporters import CsvExporter, HtmlExporter

def choose_pricing_strategy(student: Student, course_dept: str) -> IPricingStrategy:
    """
    הלוגיקה של *בחירת* האסטרטגיה נמצאת אצל הלקוח (Client), לא ב-Service.
    הוצאנו אותה לפונקציה כדי שנוכל לבדוק אותה ב-PyTest.
    """
    if student.is_excellent:
        return PercentageDiscountStrategy(25)
    if student.department == "cs" and course_dept == "cs":
        return PercentageDiscountStrategy(10)
    if student.department == "math" and course_dept == "math":
        return FixedDiscountStrategy(20)
    return DefaultStrategy()


def select_student(students: dict) -> Student:
    """בחירת הסטודנט המחובר (במקום מערכת התחברות אמיתית)."""
    print("Choose a student:")
    for key, s in students.items():
        print(f"  {key}) {s}")
    while True:
        choice = input("> ").strip()
        if choice in students:
            return students[choice]
        print("Invalid choice, try again.")


def main():
    # 1. שלב ההרכבה (Composition) - כאן יוצרים את כל האובייקטים
    service = CourseService(db=COURSES_DB)
    exporters = {"html": HtmlExporter(), "csv": CsvExporter()}
    students = {
        "1": Student("1", "Dana", "cs"),
        "2": Student("2", "Yossi", "math"),
        "3": Student("3", "Noa", "cs", is_excellent=True),
    }
    student = select_student(students)

    # 2. שלב הריצה (Execution)
    print("Welcome to the Course Search Engine")
    while True:
        dept = input("Enter department (cs/math) or 'q' to quit: ").strip().lower()

        if dept == "q":
            print("Goodbye!")
            break

        courses = service.find_courses_by_dept(dept)

        if courses is None:
            print(f"Error: Department '{dept}' not found.")
            continue

        print(f"--- Courses in '{dept}' ---")

        if not courses:
            print("No courses found.")
            continue

        # האסטרטגיה תלויה בסטודנט ובמחלקה בלבד, אז בוחרים אותה פעם אחת
        strategy = choose_pricing_strategy(student, dept)

        for course in courses:
            prereq_str = service.get_formatted_prereqs(course)
            final_price = service.calculate_price(strategy, course["price"])
            print(f"> ID: {course['id']}, Name: {course['name']}, "
                  f"Prereqs: {prereq_str}, Price: {final_price:.2f}")

        print("-" * (len(dept) + 18) + "\n")

        # ייצוא - Template Method
        fmt = input("Export report? (html/csv, Enter to skip): ").strip().lower()
        exporter = exporters.get(fmt)
        if exporter:
            print(exporter.export(courses))


if __name__ == "__main__":
    main()
