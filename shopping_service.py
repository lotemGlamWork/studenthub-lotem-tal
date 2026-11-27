# shopping_service.py - STU-203: עגלת קניות
from strategies import IPricingStrategy, DefaultStrategy


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

    def remove_from_cart(self, course_id):
        """
        STU-301:
        True  - הקורס היה בעגלה והוסר.
        False - הקורס לא בעגלה (גם מזהה שלא קיים בכלל); בלי שגיאה.
        """
        for i, item in enumerate(self._cart):
            if item["id"] == course_id:
                del self._cart[i]
                return True
        return False

    def get_cart(self):
        """עותק של תוכן העגלה, כדי שלא ישנו אותה מבחוץ."""
        return list(self._cart)

    def calculate_total(self, strategy: IPricingStrategy):
        """סכום המחירים של כל הקורסים בעגלה אחרי הפעלת האסטרטגיה על כל קורס."""
        return sum(strategy.calculate_price(course["price"]) for course in self._cart)

    def get_item_count(self):
        """STU-302: מספר הקורסים בעגלה."""
        return len(self._cart)

    def get_subtotal(self):
        """STU-302: סכום המחירים המקוריים, לפני הנחה."""
        return self.calculate_total(DefaultStrategy())

    def calculate_savings(self, strategy: IPricingStrategy):
        """STU-302: כמה חוסכים - סכום מקורי פחות הסכום אחרי ההנחה."""
        return self.get_subtotal() - self.calculate_total(strategy)
