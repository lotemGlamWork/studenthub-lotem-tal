# test_strategies.py
import pytest
from strategies import (
    IPricingStrategy,
    DefaultStrategy,
    FixedDiscountStrategy,
    PercentageDiscountStrategy,
)
from services import CourseService
from student import Student
from main import choose_pricing_strategy


# --- חלק א': כל אסטרטגיה נבדקת לבד, בלי Service ובלי DB ---

def test_percentage_discount():
    strategy = PercentageDiscountStrategy(10)
    # pytest.approx: חישובי float לא תמיד מדויקים עד הספרה האחרונה
    assert strategy.calculate_price(200) == pytest.approx(180)


def test_percentage_zero_means_no_discount():
    assert PercentageDiscountStrategy(0).calculate_price(100) == pytest.approx(100)


def test_fixed_discount():
    assert FixedDiscountStrategy(20).calculate_price(100) == 80


def test_fixed_discount_never_below_zero():
    # מקרה קצה: ההנחה גדולה מהמחיר
    assert FixedDiscountStrategy(20).calculate_price(15) == 0


def test_default_strategy_returns_base_price():
    assert DefaultStrategy().calculate_price(100) == 100


def test_interface_cannot_be_instantiated():
    # ה"חוזה" הוא מחלקה אבסטרקטית - אי אפשר ליצור ממנו מופע
    with pytest.raises(TypeError):
        IPricingStrategy()


# --- חלק ב': ה-Service רק מאציל (delegates) לאסטרטגיה ---

class SpyStrategy(IPricingStrategy):
    """Test Double מסוג Spy: מתעד איך קראו לו ומחזיר ערך קבוע."""
    def __init__(self):
        self.received_price = None

    def calculate_price(self, base_price):
        self.received_price = base_price
        return 42


def test_service_delegates_to_strategy():
    spy = SpyStrategy()
    service = CourseService(db={})  # ה-DB לא רלוונטי לבדיקה הזו

    result = service.calculate_price(spy, 100)

    assert result == 42               # ה-Service החזיר את מה שהאסטרטגיה חישבה
    assert spy.received_price == 100  # והעביר לה את המחיר הנכון


# --- חלק ג': הלוגיקה של בחירת האסטרטגיה (אצל ה-Client) ---

@pytest.mark.parametrize("student, course_dept, expected_price", [
    (Student("1", "Noa",   "cs",   is_excellent=True), "math", 75),   # מצטיין: 25% על הכל
    (Student("2", "Noa",   "cs",   is_excellent=True), "cs",   75),   # מצטיין גובר על הנחת חוג
    (Student("3", "Dana",  "cs"),                      "cs",   90),   # מדמ"ח בקורס מדמ"ח
    (Student("4", "Yossi", "math"),                    "math", 80),   # מתמטיקה: 20 ש"ח
    (Student("5", "Dana",  "cs"),                      "math", 100),  # בלי הנחה
    (Student("6", "Yossi", "math"),                    "cs",   100),  # בלי הנחה
])
def test_choose_pricing_strategy(student, course_dept, expected_price):
    strategy = choose_pricing_strategy(student, course_dept)
    assert strategy.calculate_price(100) == pytest.approx(expected_price)
