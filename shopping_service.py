# shopping_service.py - STU-203: עגלת קניות
from strategies import IPricingStrategy


class ShoppingService:
    """
    עגלת קניות של קורסים.
    מקבלת את CourseService מבחוץ (Dependency Injection) ומשתמשת בו רק כדי לאתר קורסים.
    חוקי ההנחה לא נמצאים כאן: מקבלים IPricingStrategy מבחוץ (Strategy Pattern).
    """

    def __init__(self, course_service):
        self.course_service = course_service
        self._cart = []  # רשימת dict-ים של קורסים, לפי סדר ההוספה

    def add_to_cart(self, course_id):
        """
        True  - הקורס נוסף.
        False - הקורס כבר בעגלה (לא מוסיפים כפילות).
        ValueError - אין קורס כזה; העגלה לא משתנה.
        """
        course = self.course_service.get_course_by_id(course_id)
        if course is None:
            raise ValueError(f"Course '{course_id}' not found")
        if any(item["id"] == course_id for item in self._cart):
            return False
        self._cart.append(course)
        return True

    def get_cart(self):
        """עותק של תוכן העגלה, כדי שלא ישנו אותה מבחוץ."""
        return list(self._cart)

    def calculate_total(self, strategy: IPricingStrategy):
        """סכום המחירים של כל הקורסים בעגלה אחרי הפעלת האסטרטגיה על כל קורס."""
        return sum(strategy.calculate_price(course["price"]) for course in self._cart)
