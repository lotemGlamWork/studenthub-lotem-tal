# shopping_service.py - STU-203: עגלת קניות
from strategies import IPricingStrategy, DefaultStrategy
from exporters import BaseReportExporter


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

    def clear_cart(self):
        """STU-304: מרוקן את העגלה ומחזיר כמה קורסים הוסרו (0 אם כבר ריקה)."""
        removed = len(self._cart)
        self._cart.clear()
        return removed

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

    def export_cart(self, exporter: BaseReportExporter, filepath):
        """
        STU-303: מייצא את הקורסים שבעגלה לקובץ.
        הפורמט כולו אצל ה-exporter (Template Method); כאן רק כותבים את התוצאה לקובץ.
        עגלה ריקה מייצאת דוח עם כותרת וסיום בלבד. מחזיר את הנתיב שנכתב.
        """
        content = exporter.export(self.get_cart())
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        return filepath

    def checkout(self, student, strategy: IPricingStrategy):
        """
        STU-305: מסיים רכישה.
        מחשב את הסכום עם האסטרטגיה, רושם את הסטודנט לכל הקורסים שבעגלה
        (Student.add_course כבר מונע כפילויות), מרוקן את העגלה ומחזיר קבלה.
        עגלה ריקה -> ValueError, בלי לשנות דבר.
        """
        if self.get_item_count() == 0:
            raise ValueError("Cannot checkout: the cart is empty")

        items = self.get_cart()
        subtotal = self.get_subtotal()
        total_paid = self.calculate_total(strategy)

        newly_enrolled = []
        already_enrolled = []
        for course in items:
            if student.add_course(course["id"]):
                newly_enrolled.append(course["id"])
            else:
                already_enrolled.append(course["id"])

        self.clear_cart()
        return {
            "student_id": student.id,
            "items_count": len(items),
            "enrolled_count": len(newly_enrolled),
            "enrolled_courses": newly_enrolled,
            "already_enrolled": already_enrolled,
            "subtotal": subtotal,
            "savings": subtotal - total_paid,
            "total_paid": total_paid,
        }
