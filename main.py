# main.py - V5: STU-202 - מחיר אמיתי לכל קורס
# מה השתנה מ-step-1?
#   הקבוע BASE_PRICE נמחק. כל קורס מגיע עם "price" משלו מ-data.py.
from data import COURSES_DB
from services import CourseService
from shopping_service import ShoppingService
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


def print_cart(cart: ShoppingService, student: Student) -> None:
    """STU-203/302: מדפיס את תוכן העגלה וסיכום: פריטים, סכום מקורי, חיסכון וסכום סופי."""
    items = cart.get_cart()
    if not items:
        print("Your cart is empty.")
        print("Items in cart: 0\n")
        return
    print("--- Your cart ---")
    for course in items:
        print(f"> ID: {course['id']}, Name: {course['name']}, Price: {course['price']:.2f}")
    # בחירת האסטרטגיה נשארת אצל הלקוח; העגלה רק מפעילה אותה
    strategy = choose_pricing_strategy(student, student.department)
    print("-" * 17)
    print(f"Items in cart: {cart.get_item_count()}")
    print(f"Subtotal: {cart.get_subtotal():.2f}")
    print(f"Savings: {cart.calculate_savings(strategy):.2f}")
    print(f"Total: {cart.calculate_total(strategy):.2f}\n")


def remove_from_cart(cart: ShoppingService, course_id: str) -> None:
    """STU-301: מסיר קורס מהעגלה ומדפיס משוב ברור."""
    if not course_id:
        print("No course id given, nothing removed.\n")
    elif cart.remove_from_cart(course_id):
        print(f"Course {course_id} removed from cart.\n")
    else:
        print(f"Course {course_id} is not in the cart.\n")


def main():
    # 1. שלב ההרכבה (Composition) - כאן יוצרים את כל האובייקטים
    service = CourseService(db=COURSES_DB)
    cart = ShoppingService(course_service=service)
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
        command = input(
            "Enter department (cs/math), 'cart', 'remove <id>' or 'q' to quit: "
        ).strip()
        dept = command.lower()

        if dept == "q":
            print("Goodbye!")
            break

        if dept == "cart":
            print_cart(cart, student)
            continue

        # STU-301: 'remove <id>' או 'remove' ואז שאלה על המזהה
        if dept == "remove" or dept.startswith("remove "):
            course_id = command[len("remove"):].strip()
            if not course_id:
                course_id = input("Course id to remove: ").strip()
            remove_from_cart(cart, course_id)
            continue

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

        # STU-203: הוספה לעגלה
        course_id = input("Add a course to cart? (id, Enter to skip): ").strip()
        if course_id:
            try:
                if cart.add_to_cart(course_id):
                    print(f"Course {course_id} added to cart.")
                else:
                    print(f"Course {course_id} is already in the cart.")
            except ValueError as e:
                print(f"Error: {e}")

        # ייצוא - Template Method
        fmt = input("Export report? (html/csv, Enter to skip): ").strip().lower()
        exporter = exporters.get(fmt)
        if exporter:
            print(exporter.export(courses))


if __name__ == "__main__":
    main()
